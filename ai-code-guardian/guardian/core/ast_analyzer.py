"""
AST 分析器模块

使用 Python 内置 ast 模块解析源码，提取函数/方法的结构化信息。
这是所有分析模块的共享基础设施。
"""

from __future__ import annotations

import ast
import textwrap
from dataclasses import dataclass, field


@dataclass
class ParameterInfo:
    """函数参数的结构化信息，用于精确的逐参数对比"""
    name: str
    annotation: str | None = None     # 类型注解字符串，如 "int", "list[str]"
    default: str | None = None        # 默认值字符串，如 "'hello'", "None"
    kind: str = "POSITIONAL_OR_KEYWORD"  # POSITIONAL_ONLY / POSITIONAL_OR_KEYWORD / VAR_POSITIONAL / KEYWORD_ONLY / VAR_KEYWORD


@dataclass
class APISignature:
    """公开 API 签名的结构化表示，用于 APIDiff 对比引擎"""
    name: str                          # 函数名
    qualified_name: str                # 限定名，如 "MyClass.my_method"
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_annotation: str | None = None
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False
    is_public: bool = True
    file_path: str = "<unknown>"
    line_start: int = 0


@dataclass
class FunctionInfo:
    """函数/方法的结构化信息"""
    name: str
    file_path: str
    line_start: int
    line_end: int
    signature: str              # 如: def foo(a: int, b: str = "x") -> bool
    docstring: str | None
    body_source: str            # 函数体源码
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False
    parent_class: str | None = None  # 如果是方法，记录所在类名
    is_public: bool = True      # 是否为公开 API（不以 _ 开头）


class ASTAnalyzer:
    """Python 源码 AST 分析器

    从源码字符串中提取函数和方法的结构化信息，
    支持新旧版本对比以检测变更。
    """

    def extract_functions(self, source: str, filepath: str = "<unknown>") -> list[FunctionInfo]:
        """从源码中提取所有函数/方法信息。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径（用于记录）。

        Returns:
            FunctionInfo 对象列表。
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        source_lines = source.splitlines()
        functions: list[FunctionInfo] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_info = self._extract_function_info(node, source_lines, filepath)
                functions.append(func_info)

        return functions

    def extract_functions_with_context(
        self, source: str, filepath: str = "<unknown>"
    ) -> list[FunctionInfo]:
        """从源码中提取函数信息，同时保留类的层级关系。

        与 extract_functions 类似，但会正确设置 parent_class。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径。

        Returns:
            FunctionInfo 对象列表。
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        source_lines = source.splitlines()
        functions: list[FunctionInfo] = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_info = self._extract_function_info(node, source_lines, filepath)
                functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        func_info = self._extract_function_info(
                            child, source_lines, filepath, parent_class=class_name
                        )
                        functions.append(func_info)

        return functions

    def diff_functions(
        self, old_source: str, new_source: str, filepath: str = "<unknown>"
    ) -> dict[str, list[FunctionInfo]]:
        """对比两个版本的源码，返回新增/删除/修改的函数。

        Args:
            old_source: 旧版本源码。
            new_source: 新版本源码。
            filepath: 文件路径。

        Returns:
            包含四个键的字典：
            - "added": 新增的函数
            - "removed": 删除的函数
            - "modified": 修改的函数（签名或函数体变化）
            - "unchanged": 未变化的函数
        """
        old_funcs = {f.name: f for f in self.extract_functions_with_context(old_source, filepath)}
        new_funcs = {f.name: f for f in self.extract_functions_with_context(new_source, filepath)}

        old_names = set(old_funcs.keys())
        new_names = set(new_funcs.keys())

        added = [new_funcs[name] for name in (new_names - old_names)]
        removed = [old_funcs[name] for name in (old_names - new_names)]

        modified = []
        unchanged = []

        for name in old_names & new_names:
            old_func = old_funcs[name]
            new_func = new_funcs[name]

            if (old_func.signature != new_func.signature or
                    old_func.body_source != new_func.body_source):
                modified.append(new_func)
            else:
                unchanged.append(new_func)

        return {
            "added": added,
            "removed": removed,
            "modified": modified,
            "unchanged": unchanged,
        }

    def extract_public_api(self, source: str, filepath: str = "<unknown>") -> list[FunctionInfo]:
        """提取公开 API 清单（不以 _ 开头的函数/类方法）。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径。

        Returns:
            公开 API 的 FunctionInfo 列表。
        """
        all_funcs = self.extract_functions_with_context(source, filepath)
        return [f for f in all_funcs if f.is_public]

    def extract_api_signatures(
        self, source: str, filepath: str = "<unknown>", public_only: bool = True
    ) -> list[APISignature]:
        """从源码中提取结构化的 API 签名列表。

        这是 T2.1 增强版本，为 APIDiff 对比引擎提供精确的逐参数对比数据。

        Args:
            source: Python 源码字符串。
            filepath: 源文件路径。
            public_only: 是否仅提取公开 API（默认 True）。

        Returns:
            APISignature 对象列表。
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        signatures: list[APISignature] = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                sig = self._node_to_api_signature(node, filepath, parent_class=None)
                if not public_only or sig.is_public:
                    signatures.append(sig)
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        sig = self._node_to_api_signature(child, filepath, parent_class=class_name)
                        if not public_only or sig.is_public:
                            signatures.append(sig)

        return signatures

    def _node_to_api_signature(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        filepath: str,
        parent_class: str | None = None,
    ) -> APISignature:
        """从 AST 函数节点提取结构化 API 签名。

        Args:
            node: AST 函数定义节点。
            filepath: 源文件路径。
            parent_class: 所在类名（如果是方法）。

        Returns:
            APISignature 实例。
        """
        name = node.name
        qualified_name = f"{parent_class}.{name}" if parent_class else name

        parameters = self._extract_parameters(node.args)

        return_annotation = None
        if node.returns:
            return_annotation = self._node_to_str(node.returns)

        decorators = [self._node_to_str(d) for d in node.decorator_list]

        return APISignature(
            name=name,
            qualified_name=qualified_name,
            parameters=parameters,
            return_annotation=return_annotation,
            decorators=decorators,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_public=not name.startswith("_"),
            file_path=filepath,
            line_start=node.lineno,
        )

    def _extract_parameters(self, args: ast.arguments) -> list[ParameterInfo]:
        """从 ast.arguments 中提取结构化的参数信息列表。

        Args:
            args: AST 参数节点。

        Returns:
            ParameterInfo 列表，按参数顺序排列。
        """
        params: list[ParameterInfo] = []

        # positional-only 参数
        for arg in args.posonlyargs:
            params.append(ParameterInfo(
                name=arg.arg,
                annotation=self._node_to_str(arg.annotation) if arg.annotation else None,
                kind="POSITIONAL_ONLY",
            ))

        # 普通参数 (positional or keyword)
        num_args = len(args.args)
        num_defaults = len(args.defaults)
        default_offset = num_args - num_defaults

        for i, arg in enumerate(args.args):
            default = None
            default_idx = i - default_offset
            if 0 <= default_idx < len(args.defaults):
                default = self._node_to_str(args.defaults[default_idx])

            params.append(ParameterInfo(
                name=arg.arg,
                annotation=self._node_to_str(arg.annotation) if arg.annotation else None,
                default=default,
                kind="POSITIONAL_OR_KEYWORD",
            ))

        # *args
        if args.vararg:
            params.append(ParameterInfo(
                name=args.vararg.arg,
                annotation=self._node_to_str(args.vararg.annotation) if args.vararg.annotation else None,
                kind="VAR_POSITIONAL",
            ))

        # keyword-only 参数
        for i, arg in enumerate(args.kwonlyargs):
            default = None
            if i < len(args.kw_defaults) and args.kw_defaults[i] is not None:
                default = self._node_to_str(args.kw_defaults[i])

            params.append(ParameterInfo(
                name=arg.arg,
                annotation=self._node_to_str(arg.annotation) if arg.annotation else None,
                default=default,
                kind="KEYWORD_ONLY",
            ))

        # **kwargs
        if args.kwarg:
            params.append(ParameterInfo(
                name=args.kwarg.arg,
                annotation=self._node_to_str(args.kwarg.annotation) if args.kwarg.annotation else None,
                kind="VAR_KEYWORD",
            ))

        return params

    # ──────────────────────────────────────
    # 内部辅助方法
    # ──────────────────────────────────────

    def _extract_function_info(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        source_lines: list[str],
        filepath: str,
        parent_class: str | None = None,
    ) -> FunctionInfo:
        """从 AST 节点中提取函数信息。

        Args:
            node: AST 函数定义节点。
            source_lines: 源码按行分割的列表。
            filepath: 源文件路径。
            parent_class: 所在类名（如果是方法）。

        Returns:
            FunctionInfo 实例。
        """
        name = node.name
        line_start = node.lineno
        line_end = node.end_lineno or node.lineno

        # 提取签名
        signature = self._build_signature(node)

        # 提取 docstring
        docstring = ast.get_docstring(node)

        # 提取函数体源码
        body_source = self._extract_body_source(source_lines, line_start, line_end)

        # 提取装饰器
        decorators = [self._node_to_str(d) for d in node.decorator_list]

        # 判断是否为公开 API
        is_public = not name.startswith("_")

        return FunctionInfo(
            name=name,
            file_path=filepath,
            line_start=line_start,
            line_end=line_end,
            signature=signature,
            docstring=docstring,
            body_source=body_source,
            decorators=decorators,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            parent_class=parent_class,
            is_public=is_public,
        )

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """从 AST 节点构建函数签名字符串。

        Args:
            node: AST 函数定义节点。

        Returns:
            签名字符串，如 "def foo(a: int, b: str = 'x') -> bool"
        """
        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        args_str = self._args_to_str(node.args)
        returns_str = ""
        if node.returns:
            returns_str = f" -> {self._node_to_str(node.returns)}"

        return f"{prefix} {node.name}({args_str}){returns_str}"

    def _args_to_str(self, args: ast.arguments) -> str:
        """将 ast.arguments 转换为字符串表示。

        Args:
            args: AST 参数节点。

        Returns:
            参数字符串。
        """
        parts: list[str] = []

        # 计算默认值的偏移量
        num_args = len(args.args)
        num_defaults = len(args.defaults)
        default_offset = num_args - num_defaults

        for i, arg in enumerate(args.args):
            part = arg.arg
            if arg.annotation:
                part += f": {self._node_to_str(arg.annotation)}"

            # 检查是否有默认值
            default_idx = i - default_offset
            if default_idx >= 0 and default_idx < len(args.defaults):
                default_val = self._node_to_str(args.defaults[default_idx])
                part += f" = {default_val}"

            parts.append(part)

        # *args
        if args.vararg:
            vararg = f"*{args.vararg.arg}"
            if args.vararg.annotation:
                vararg += f": {self._node_to_str(args.vararg.annotation)}"
            parts.append(vararg)

        # keyword-only args
        for i, arg in enumerate(args.kwonlyargs):
            part = arg.arg
            if arg.annotation:
                part += f": {self._node_to_str(arg.annotation)}"
            if i < len(args.kw_defaults) and args.kw_defaults[i] is not None:
                part += f" = {self._node_to_str(args.kw_defaults[i])}"
            parts.append(part)

        # **kwargs
        if args.kwarg:
            kwarg = f"**{args.kwarg.arg}"
            if args.kwarg.annotation:
                kwarg += f": {self._node_to_str(args.kwarg.annotation)}"
            parts.append(kwarg)

        return ", ".join(parts)

    def _node_to_str(self, node: ast.AST) -> str:
        """将 AST 节点转换为字符串表示。

        尽可能使用 ast.unparse（Python 3.9+），否则回退到简单表示。

        Args:
            node: AST 节点。

        Returns:
            节点的字符串表示。
        """
        try:
            return ast.unparse(node)
        except (AttributeError, ValueError):
            return repr(node)

    def _extract_body_source(
        self, source_lines: list[str], line_start: int, line_end: int
    ) -> str:
        """从源码行中提取函数体。

        Args:
            source_lines: 源码按行分割的列表。
            line_start: 起始行号（1-based）。
            line_end: 结束行号（1-based）。

        Returns:
            函数体源码字符串。
        """
        if line_start > len(source_lines) or line_end > len(source_lines):
            return ""

        body_lines = source_lines[line_start - 1: line_end]
        return "\n".join(body_lines)
