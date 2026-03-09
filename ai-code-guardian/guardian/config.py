"""
Guardian 配置管理模块

支持从 .guardian.yaml 文件加载配置，并在配置缺失时提供合理的默认值回退。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ──────────────────────────────────────────
# 配置数据类
# ──────────────────────────────────────────

@dataclass
class TestGenConfig:
    """AI 测试生成模块配置"""
    enabled: bool = True
    output_dir: str = "tests/auto_generated"
    mutation_testing: bool = False
    max_tests_per_function: int = 5


@dataclass
class ApiDiffConfig:
    """API 破坏性变更检测模块配置"""
    enabled: bool = True
    strict_mode: bool = True
    ignore_patterns: list[str] = field(default_factory=lambda: ["_internal_*", "test_*"])


@dataclass
class PerfGuardConfig:
    """性能退化守卫模块配置"""
    enabled: bool = True
    threshold_warning: float = 0.10
    threshold_fail: float = 0.30
    benchmark_timeout: int = 30


@dataclass
class I18nGuardConfig:
    """国际化硬编码审查模块配置"""
    enabled: bool = True
    target_langs: list[str] = field(default_factory=lambda: ["en", "ja"])
    key_style: str = "namespace"
    output_format: str = "json"
    locale_dir: str = "locales/"
    skip_patterns: list[str] = field(default_factory=lambda: [r"logger\.", "# "])


@dataclass
class GuardianConfig:
    """Guardian 全局配置"""
    enabled: bool = True
    llm_provider: str = "claude"
    llm_model: str = "claude-sonnet-4-20250514"
    test_gen: TestGenConfig = field(default_factory=TestGenConfig)
    api_diff: ApiDiffConfig = field(default_factory=ApiDiffConfig)
    perf_guard: PerfGuardConfig = field(default_factory=PerfGuardConfig)
    i18n_guard: I18nGuardConfig = field(default_factory=I18nGuardConfig)


# ──────────────────────────────────────────
# 配置加载逻辑
# ──────────────────────────────────────────

DEFAULT_CONFIG_FILENAME = ".guardian.yaml"


def _find_config_file(start_dir: str | Path | None = None) -> Path | None:
    """从给定目录向上查找 .guardian.yaml 配置文件。

    Args:
        start_dir: 起始搜索目录，默认为当前工作目录。

    Returns:
        找到的配置文件路径，未找到则返回 None。
    """
    current = Path(start_dir or os.getcwd()).resolve()

    while True:
        config_path = current / DEFAULT_CONFIG_FILENAME
        if config_path.is_file():
            return config_path
        parent = current.parent
        if parent == current:
            # 已到达文件系统根目录
            break
        current = parent

    return None


def _parse_sub_config(data: dict[str, Any], cls: type, defaults: Any) -> Any:
    """将字典数据解析为指定的数据类实例。

    Args:
        data: 原始字典数据。
        cls: 目标数据类。
        defaults: 默认实例（未提供的字段使用默认值）。

    Returns:
        数据类实例。
    """
    if not data:
        return defaults

    valid_fields = {f_name for f_name in cls.__dataclass_fields__}
    filtered = {k: v for k, v in data.items() if k in valid_fields}

    # 从默认值构建基础，再用用户配置覆盖
    base = {f_name: getattr(defaults, f_name) for f_name in cls.__dataclass_fields__}
    base.update(filtered)
    return cls(**base)


def load_config(config_path: str | Path | None = None) -> GuardianConfig:
    """加载 Guardian 配置。

    优先级：
    1. 明确指定的配置文件路径
    2. 从当前目录向上搜索 .guardian.yaml
    3. 使用默认配置

    Args:
        config_path: 可选的配置文件路径。

    Returns:
        解析后的 GuardianConfig 实例。
    """
    defaults = GuardianConfig()

    # 确定配置文件位置
    if config_path:
        path = Path(config_path)
        if not path.is_file():
            return defaults
    else:
        path = _find_config_file()
        if path is None:
            return defaults

    # 读取并解析 YAML
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    except (yaml.YAMLError, OSError):
        return defaults

    if not raw or not isinstance(raw, dict):
        return defaults

    # 配置可能嵌套在 "guardian" 键下
    guardian_data = raw.get("guardian", raw)

    # 解析顶层配置
    config = GuardianConfig(
        enabled=guardian_data.get("enabled", defaults.enabled),
        llm_provider=guardian_data.get("llm_provider", defaults.llm_provider),
        llm_model=guardian_data.get("llm_model", defaults.llm_model),
        test_gen=_parse_sub_config(
            guardian_data.get("test_gen", {}), TestGenConfig, defaults.test_gen
        ),
        api_diff=_parse_sub_config(
            guardian_data.get("api_diff", {}), ApiDiffConfig, defaults.api_diff
        ),
        perf_guard=_parse_sub_config(
            guardian_data.get("perf_guard", {}), PerfGuardConfig, defaults.perf_guard
        ),
        i18n_guard=_parse_sub_config(
            guardian_data.get("i18n_guard", {}), I18nGuardConfig, defaults.i18n_guard
        ),
    )

    return config
