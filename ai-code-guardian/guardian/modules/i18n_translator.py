"""
I18n 翻译器 - LLM 驱动的中文字符串翻译

利用 LLM 将硬编码的中文字符串翻译为英文，
并生成 i18n key 建议和替换代码建议。
"""

from __future__ import annotations

from dataclasses import dataclass

from guardian.core.llm_client import LLMClient, LLMMessage
from guardian.modules.i18n_guard import HardcodedString


# ── 翻译 Prompt 模板 ──────────────────────

SYSTEM_PROMPT = """你是一个专业的国际化（i18n）翻译助手。
你的任务是将代码中的中文硬编码字符串翻译为英文，并建议 i18n key。

规则：
1. 翻译要自然、符合英语编程习惯
2. i18n key 使用 snake_case 格式
3. 保持简洁，避免过长的 key
4. 输出严格的 JSON 格式"""

TRANSLATE_PROMPT_TEMPLATE = """请翻译以下代码中的中文字符串，并为每个字符串建议 i18n key 和英文翻译。

文件: {filepath}

需要翻译的字符串列表:
{strings_block}

请以 JSON 数组格式返回，每个元素包含:
- "original": 原始中文字符串
- "key": 建议的 i18n key (snake_case)
- "translation": 英文翻译
- "context_note": 简短的上下文说明

示例输出:
[
  {{
    "original": "用户名不能为空",
    "key": "error.username_required",
    "translation": "Username cannot be empty",
    "context_note": "Form validation error"
  }}
]"""


@dataclass
class TranslationResult:
    """翻译结果"""
    original: str
    key: str
    translation: str
    context_note: str = ""


class I18nTranslator:
    """LLM 驱动的 i18n 翻译器"""

    def __init__(self, llm_client: LLMClient) -> None:
        """初始化翻译器。

        Args:
            llm_client: LLM 客户端实例。
        """
        self.llm = llm_client

    def translate_batch(
        self,
        strings: list[HardcodedString],
        filepath: str = "<unknown>",
    ) -> list[TranslationResult]:
        """批量翻译硬编码字符串。

        Args:
            strings: 需要翻译的字符串列表。
            filepath: 文件路径。

        Returns:
            TranslationResult 列表。
        """
        if not strings:
            return []

        # 构建字符串块
        lines = []
        for i, s in enumerate(strings, 1):
            lines.append(f"{i}. \"{s.value}\" (行 {s.line})")
        strings_block = "\n".join(lines)

        # 构建 prompt
        user_prompt = TRANSLATE_PROMPT_TEMPLATE.format(
            filepath=filepath,
            strings_block=strings_block,
        )

        # 调用 LLM
        messages = [
            LLMMessage(role="system", content=SYSTEM_PROMPT),
            LLMMessage(role="user", content=user_prompt),
        ]

        try:
            response = self.llm.chat(messages, temperature=0.1, max_tokens=2000)
            return self._parse_translation_response(response.content, strings)
        except Exception:
            # LLM 不可用时，返回空翻译
            return [
                TranslationResult(
                    original=s.value,
                    key=s.suggested_key or f"untranslated_{i}",
                    translation="",
                    context_note="LLM 不可用，需手动翻译",
                )
                for i, s in enumerate(strings)
            ]

    def _parse_translation_response(
        self, content: str, original_strings: list[HardcodedString]
    ) -> list[TranslationResult]:
        """解析 LLM 返回的 JSON 翻译结果。

        Args:
            content: LLM 响应内容。
            original_strings: 原始字符串列表。

        Returns:
            TranslationResult 列表。
        """
        import json

        # 尝试提取 JSON 部分
        content = content.strip()
        if content.startswith("```"):
            # 去除 markdown 代码块
            lines = content.split("\n")
            json_lines = []
            in_block = False
            for line in lines:
                if line.startswith("```"):
                    in_block = not in_block
                    continue
                if in_block or not line.startswith("```"):
                    json_lines.append(line)
            content = "\n".join(json_lines)

        try:
            results = json.loads(content)
        except json.JSONDecodeError:
            # 解析失败，返回空结果
            return [
                TranslationResult(
                    original=s.value,
                    key=s.suggested_key or f"parse_error_{i}",
                    translation="",
                    context_note="LLM 响应解析失败",
                )
                for i, s in enumerate(original_strings)
            ]

        translations = []
        for item in results:
            translations.append(TranslationResult(
                original=item.get("original", ""),
                key=item.get("key", ""),
                translation=item.get("translation", ""),
                context_note=item.get("context_note", ""),
            ))

        return translations
