"""
LLM 客户端基建

提供与大语言模型交互的通用接口，
支持 OpenAI 兼容 API（包括 Azure OpenAI、本地模型等）。
"""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LLMMessage:
    """LLM 对话消息"""
    role: str       # "system" / "user" / "assistant"
    content: str


@dataclass
class LLMResponse:
    """LLM 响应"""
    content: str
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)  # prompt_tokens, completion_tokens, total_tokens
    raw: dict | None = None


class LLMClient(ABC):
    """LLM 客户端抽象基类"""

    @abstractmethod
    def chat(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        """发送聊天请求。

        Args:
            messages: 消息列表。
            **kwargs: 额外参数（temperature, max_tokens 等）。

        Returns:
            LLMResponse 实例。
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """检查 LLM 服务是否可用。

        Returns:
            True 表示可用。
        """
        ...


class OpenAICompatibleClient(LLMClient):
    """OpenAI 兼容 API 客户端

    支持任何遵循 OpenAI Chat Completions API 格式的服务：
    - OpenAI
    - Azure OpenAI
    - 本地模型（Ollama, vLLM 等）
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-3.5-turbo",
        timeout: int = 30,
    ) -> None:
        """初始化 OpenAI 兼容客户端。

        Args:
            api_key: API 密钥。默认从环境变量 OPENAI_API_KEY 读取。
            base_url: API 基础 URL。
            model: 模型名称。
            timeout: 请求超时（秒）。
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        """发送 Chat Completions 请求。

        Args:
            messages: 消息列表。
            **kwargs: temperature, max_tokens 等。

        Returns:
            LLMResponse 实例。

        Raises:
            RuntimeError: API 调用失败。
        """
        import urllib.request
        import urllib.error

        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }

        # 可选参数
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM API 错误 ({e.code}): {body}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"LLM API 连接失败: {e.reason}") from e

        # 解析响应
        content = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})

        return LLMResponse(
            content=content,
            model=result.get("model", self.model),
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            raw=result,
        )

    def is_available(self) -> bool:
        """检查 API 是否可访问。

        Returns:
            True 表示可用。
        """
        if not self.api_key:
            return False
        try:
            # 发送一个简单请求测试连通性
            self.chat(
                [LLMMessage(role="user", content="ping")],
                max_tokens=1,
            )
            return True
        except Exception:
            return False


class MockLLMClient(LLMClient):
    """模拟 LLM 客户端，用于测试和离线模式。

    返回预设响应或基于简单规则的响应。
    """

    def __init__(self, responses: list[str] | None = None) -> None:
        """初始化模拟客户端。

        Args:
            responses: 预设的响应列表，按顺序返回。
        """
        self._responses = responses or ["[Mock LLM Response]"]
        self._call_count = 0

    def chat(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        """返回预设响应。

        Args:
            messages: 消息列表（忽略）。

        Returns:
            LLMResponse 实例。
        """
        idx = self._call_count % len(self._responses)
        self._call_count += 1

        return LLMResponse(
            content=self._responses[idx],
            model="mock-model",
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )

    def is_available(self) -> bool:
        return True


def create_llm_client(config: dict) -> LLMClient:
    """工厂方法：根据配置创建 LLM 客户端。

    Args:
        config: LLM 配置字典，支持以下键：
            - provider: "openai" / "mock"（默认 "openai"）
            - api_key: API 密钥
            - base_url: API 地址
            - model: 模型名称
            - timeout: 超时秒数

    Returns:
        LLMClient 实例。
    """
    provider = config.get("provider", "openai")

    if provider == "mock":
        return MockLLMClient(responses=config.get("mock_responses"))

    return OpenAICompatibleClient(
        api_key=config.get("api_key"),
        base_url=config.get("base_url", "https://api.openai.com/v1"),
        model=config.get("model", "gpt-3.5-turbo"),
        timeout=config.get("timeout", 30),
    )
