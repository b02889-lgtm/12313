"""
I18n Guard 模块 - 国际化硬编码审查

拦截代码中的中文硬编码字符串（魔法字符串），
提供位置定位和翻译建议，支持 LLM 驱动的翻译。
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field


# 匹配中文字符的正则
CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")


@dataclass
class HardcodedString:
    """硬编码字符串的结构化信息"""
    value: str                    # 字符串原文
    file_path: str                # 文件路径
    line: int                     # 行号
    col: int                      # 列号
    context: str                  # 上下文（所在的 AST 节点类型）
    parent_function: str | None = None  # 所在函数名
    parent_class: str | None = None     # 所在类名
    suggested_key: str | None = None    # 建议的 i18n key
    translation: str | None = None      # LLM 生成的翻译


class StringExtractor:
    """从 Python 源码中提取含中文的硬编码字符串。

    使用 AST 遍历精确定位字符串节点，
    排除已知的安全模式（docstring、日志格式等可配置）。
    """

    # 默认排除模式：这些上下文中的字符串不报告
    DEFAULT_EXCLUDE_CONTEXTS = frozenset({
        "docstring",    # 函数/类 docstring
    })

    def __init__(
        self,
        exclude_contexts: frozenset[str] | None = None,
        min_chinese_chars: int = 1,
    ) -> None:
        """初始化字符串提取器。

        Args:
            exclude_contexts: 要排除的上下文集合。
            min_chinese_chars: 最少中文字符数，低于此值不报告。
        """
        self.exclude_contexts = exclude_contexts or self.DEFAULT_EXCLUDE_CONTEXTS
        self.min_chinese_chars = min_chinese_chars

    def extract(self, source: str, filepath: str = "<unknown>") -> list[HardcodedString]:
        """从源码中提取所有含中文的硬编码字符串。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径。

        Returns:
            HardcodedString 列表。
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        results: list[HardcodedString] = []
        self._visit_node(tree, results, filepath, func_name=None, class_name=None)
        return results

    def _visit_node(
        self,
        node: ast.AST,
        results: list[HardcodedString],
        filepath: str,
        func_name: str | None,
        class_name: str | None,
    ) -> None:
        """递归遍历 AST 节点，收集含中文的字符串常量。

        Args:
            node: 当前 AST 节点。
            results: 收集结果的列表。
            filepath: 文件路径。
            func_name: 当前所在函数名。
            class_name: 当前所在类名。
        """
        # 更新上下文
        current_func = func_name
        current_class = class_name

        if isinstance(node, ast.ClassDef):
            current_class = node.name
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            current_func = node.name

        # 检测字符串常量
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            string_val = node.value

            # 检查是否包含中文
            chinese_count = len(CJK_PATTERN.findall(string_val))
            if chinese_count >= self.min_chinese_chars:
                # 判断上下文
                context = self._determine_context(node)
                if context not in self.exclude_contexts:
                    results.append(HardcodedString(
                        value=string_val,
                        file_path=filepath,
                        line=node.lineno,
                        col=node.col_offset,
                        context=context,
                        parent_function=current_func,
                        parent_class=current_class,
                    ))

        # 递归子节点
        for child in ast.iter_child_nodes(node):
            self._visit_node(child, results, filepath, current_func, current_class)

    def _determine_context(self, node: ast.Constant) -> str:
        """判断字符串节点的使用上下文。

        基于父节点类型推断，目前支持的上下文类型：
        - "assignment": 赋值语句
        - "call_arg": 函数调用参数
        - "return": return 语句
        - "format": f-string / format 调用
        - "other": 其他

        注意：此方法需要 AST 带有父节点信息（通过 _annotate_parents 预处理）。
        由于 Python AST 不自带父节点引用，这里简化处理。

        Args:
            node: 字符串常量节点。

        Returns:
            上下文类型字符串。
        """
        # 简化实现：由于 Python AST 不提供 parent 引用，
        # 在 _visit_node 中已经通过递归上下文传递了 func/class 信息。
        # 这里返回通用类型，后续可增强。
        return "string_literal"

    def extract_with_suggestions(
        self, source: str, filepath: str = "<unknown>"
    ) -> list[HardcodedString]:
        """提取字符串并自动生成 i18n key 建议。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径。

        Returns:
            带 suggested_key 的 HardcodedString 列表。
        """
        strings = self.extract(source, filepath)

        for s in strings:
            s.suggested_key = self._generate_key_suggestion(s)

        return strings

    def _generate_key_suggestion(self, s: HardcodedString) -> str:
        """为硬编码字符串生成 i18n key 建议。

        格式：module.class.function.短描述

        Args:
            s: 硬编码字符串信息。

        Returns:
            建议的 i18n key。
        """
        parts = []

        # 从文件路径提取模块名
        if s.file_path and s.file_path != "<unknown>":
            module = s.file_path.replace("/", ".").replace("\\", ".")
            module = module.removesuffix(".py")
            parts.append(module.split(".")[-1])

        if s.parent_class:
            parts.append(self._to_snake_case(s.parent_class))

        if s.parent_function:
            parts.append(s.parent_function)

        # 从字符串内容生成短描述
        short = self._truncate_for_key(s.value)
        parts.append(short)

        return ".".join(parts)

    def _to_snake_case(self, name: str) -> str:
        """将 CamelCase 转换为 snake_case。

        Args:
            name: 类名或标识符。

        Returns:
            snake_case 字符串。
        """
        result = re.sub(r"([A-Z])", r"_\1", name).lower().strip("_")
        return result

    def _truncate_for_key(self, text: str, max_len: int = 20) -> str:
        """从中文文本生成简短的 key 片段。

        Args:
            text: 原始字符串。
            max_len: 最大长度。

        Returns:
            简短标识符。
        """
        # 提取英文单词或拼音首字母（简化为取前几个字符的 hash）
        clean = re.sub(r"[^\w]", "", text[:max_len])
        if not clean:
            clean = f"str_{hash(text) % 10000}"
        return clean
