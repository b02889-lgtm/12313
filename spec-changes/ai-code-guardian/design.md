# 设计：AI 驱动的代码健康守护者 (AI Code Guardian)

## 1. 系统架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                       guardian-cli (入口)                            │
│                                                                     │
│  $ guardian check          # 对暂存区 (staged) 文件执行全量检查      │
│  $ guardian test-gen       # 仅执行 AI 测试生成                     │
│  $ guardian api-diff       # 仅执行 API 破坏性检测                  │
│  $ guardian perf           # 仅执行性能基准对比                     │
│  $ guardian i18n           # 仅执行硬编码审查                       │
│  $ guardian install-hook   # 安装 pre-commit hook                  │
└─────────┬──────────┬──────────┬──────────┬──────────────────────────┘
          │          │          │          │
    ┌─────▼────┐ ┌───▼────┐ ┌──▼───┐ ┌───▼────┐
    │ 模块 1   │ │ 模块 2 │ │模块 3│ │ 模块 4 │
    │ TestGen  │ │APIDiff │ │PerfGd│ │ I18nGd │
    │ (测试    │ │(API    │ │(性能 │ │(国际化 │
    │  生成)   │ │ 对比)  │ │ 守卫)│ │ 守卫)  │
    └─────┬────┘ └───┬────┘ └──┬───┘ └───┬────┘
          │          │          │          │
    ┌─────▼──────────▼──────────▼──────────▼─────┐
    │            共享基础设施层                     │
    │  ┌──────────┐ ┌────────┐ ┌───────────────┐  │
    │  │AST分析器 │ │Git适配 │ │ LLM调用器     │  │
    │  │(Python   │ │器(获取 │ │(Claude/OpenAI │  │
    │  │ ast模块) │ │diff/   │ │ 统一接口)     │  │
    │  │          │ │staged) │ │               │  │
    │  └──────────┘ └────────┘ └───────────────┘  │
    │  ┌──────────┐ ┌────────────────────────────┐ │
    │  │配置管理  │ │ 报告生成器                  │ │
    │  │(.guardian│ │ (终端彩色输出 / Markdown /  │ │
    │  │ .yaml)  │ │  JSON)                      │ │
    │  └──────────┘ └────────────────────────────┘ │
    └──────────────────────────────────────────────┘
```

## 2. 各模块详细设计

### 2.1 模块 1：AI 测试生成器 (TestGen)

**触发条件**：检测到 staged 文件中有新增或修改的 Python 函数/方法（通过 AST diff 确定）。

**工作流程**：

```
Git Staged Files
      │
      ▼
 AST 解析新旧版本
      │
      ▼
 提取变更的函数列表
 (新增函数 / 签名变更的函数)
      │
      ▼
 对每个函数，提取：
  - 函数签名 + docstring
  - 函数体代码
  - 所在文件的 import 列表
  - 相邻函数（上下文）
      │
      ▼
 构造 LLM Prompt:
 ┌──────────────────────────────────────────────┐
 │ 你是一个 Python 测试工程师。                   │
 │ 请为以下函数生成 pytest 单元测试：              │
 │                                                │
 │ [函数代码]                                     │
 │                                                │
 │ 上下文（该函数所在模块的其他函数）：            │
 │ [相邻代码]                                     │
 │                                                │
 │ 要求：                                         │
 │ 1. 覆盖正常路径、边界条件、异常输入            │
 │ 2. 使用 pytest 风格，必要时用 mock             │
 │ 3. 每个测试函数有清晰的中文注释说明测试意图    │
 └──────────────────────────────────────────────┘
      │
      ▼
 LLM 返回测试代码
      │
      ▼
 写入 tests/auto_generated/test_<module>_<func>.py
      │
      ▼
 自动运行 pytest 验证生成的测试能否通过
      │
      ▼
 输出结果：
  ✅ 为 weather_api.fetch_weather() 生成 4 个测试用例，全部通过
  ⚠️ 为 cache.TTLCache.set() 生成 3 个测试，1 个失败（需人工审查）
```

**变异测试扩展**（可选子功能）：

```python
# 变异测试原理示意
原始代码:  if temperature > 30:  return "热"
变异体1:   if temperature >= 30: return "热"    # 边界变异
变异体2:   if temperature > 30:  return "冷"    # 返回值变异
变异体3:   if temperature < 30:  return "热"    # 条件反转

# 对每个变异体运行测试套件
# 如果测试仍然通过 → 说明测试没有覆盖到这个逻辑分支 → 标记为"存活变异体"
# 变异存活率越低，测试质量越高
```

### 2.2 模块 2：API 破坏性变更检测器 (APIDiff)

**触发条件**：检测到 staged 文件中包含公开函数/类的签名修改。

**工作流程**：

```
Git Staged Files
      │
      ▼
 AST 解析旧版本 (HEAD)              AST 解析新版本 (staged)
      │                                      │
      ▼                                      ▼
 提取公开 API 清单:                   提取公开 API 清单:
 [                                   [
   func get_weather(city, units)       func get_weather(city_name, units)  ← 参数名变了！
   func format_report(data) -> str     func format_report(data) -> dict   ← 返回类型变了！
   class TTLCache                      class TTLCache
 ]                                       - 新增方法 clear()               ← 新增（非破坏性）
                                         - 删除方法 evict()               ← 删除（破坏性！）
      │                                      │
      └──────────────┬───────────────────────┘
                     │
                     ▼
              变更分类引擎
         ┌─────────────────────┐
         │ 非破坏性 (SAFE)      │  新增函数、新增可选参数、新增类方法
         │ 可能破坏 (WARNING)   │  参数重命名、参数顺序变更
         │ 确定破坏 (BREAKING)  │  删除参数、返回类型变更、删除公开方法
         └─────────────────────┘
                     │
                     ▼
              生成变更报告
         ┌─────────────────────────────────────────────┐
         │ 🔴 BREAKING: get_weather() 参数 city → city_name   │
         │    建议：保留 city 作为别名：                       │
         │    def get_weather(city_name=None, city=None): ... │
         │                                                     │
         │ 🔴 BREAKING: format_report() 返回类型 str → dict   │
         │    影响范围：3 个调用点（通过全局搜索确认）          │
         │                                                     │
         │ 🟡 WARNING: TTLCache.evict() 被删除                 │
         │    建议：标记为 @deprecated 而非直接删除             │
         │                                                     │
         │ 🟢 SAFE: TTLCache.clear() 新增                      │
         └─────────────────────────────────────────────┘
```

### 2.3 模块 3：性能退化守卫 (PerfGuard)

**触发条件**：检测到 staged 文件中有函数的逻辑变更（不仅是注释或文档修改）。

**工作流程**：

```
Git Staged Files (有逻辑变更的函数)
      │
      ▼
 检查是否存在对应的 benchmark 测试
      │
      ├── 存在 → 直接运行 benchmark
      │
      └── 不存在 → LLM 自动生成简易 benchmark
                    (基于函数签名推测合理输入)
      │
      ▼
 运行 pytest-benchmark (旧版本 vs 新版本)
      │
      ▼
 对比结果
      │
      ├── 性能差异 < 10%  → ✅ PASS
      ├── 10% ≤ 差异 < 30% → ⚠️ WARNING + 报告
      └── 差异 ≥ 30%       → 🔴 FAIL + LLM 优化建议
                                    │
                                    ▼
                          ┌──────────────────────────┐
                          │ LLM 性能优化 Prompt:      │
                          │                          │
                          │ 以下函数出现性能退化：    │
                          │ [旧代码] → [新代码]       │
                          │ 退化幅度：执行时间+45%    │
                          │                          │
                          │ 请分析原因并给出优化建议  │
                          └──────────────────────────┘
                                    │
                                    ▼
                          输出优化代码片段 + 复杂度分析
```

### 2.4 模块 4：国际化硬编码守卫 (I18nGuard)

**触发条件**：检测到 staged 的 Python 文件中存在中文字符串字面量（非注释、非 docstring）。

**工作流程**：

```
Git Staged Files
      │
      ▼
 AST 遍历所有 Str/JoinedStr 节点
      │
      ▼
 过滤规则：
  ✅ 捕获：函数体中的中文字符串（如 return "获取失败"）
  ❌ 跳过：docstring、注释、logging 格式字符串、变量名
      │
      ▼
 对每个捕获的字符串：
  - 提取所在函数名和文件路径
  - 生成基于路径的 key: weather_api.fetch_weather.error_msg
  - 调用 LLM 翻译（带上下文的 3 行代码）
      │
      ▼
 输出审查报告：
 ┌───────────────────────────────────────────────────────┐
 │ 📝 发现 3 处硬编码中文字符串：                          │
 │                                                       │
 │ 1. services/weather_api.py:45                          │
 │    原文: "获取天气信息失败"                             │
 │    建议 Key: weather_api.fetch_weather.fetch_failed    │
 │    英文翻译: "Failed to fetch weather information"     │
 │    日文翻译: "天気情報の取得に失敗しました"             │
 │    操作: [自动替换] [跳过] [自定义Key]                  │
 │                                                       │
 │ 2. tools/current.py:12                                 │
 │    原文: "错误：请提供城市名称"                         │
 │    ...                                                 │
 └───────────────────────────────────────────────────────┘
```

## 3. 共享基础设施

### 3.1 AST 分析器 (`core/ast_analyzer.py`)

所有模块都依赖对 Python 代码的静态分析，统一封装：

```python
import ast
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    name: str
    file_path: str
    line_start: int
    line_end: int
    signature: str           # def foo(a: int, b: str = "x") -> bool
    docstring: str | None
    body_source: str         # 函数体源码
    decorators: list[str]
    is_async: bool
    parent_class: str | None # 如果是方法，记录所在类名

class ASTAnalyzer:
    def extract_functions(self, source: str, filepath: str) -> list[FunctionInfo]:
        """从源码中提取所有函数/方法信息"""
        ...

    def diff_functions(self, old_source: str, new_source: str, filepath: str) -> dict:
        """对比两个版本的源码，返回新增/删除/修改的函数"""
        return {
            "added": [...],      # 新增的函数
            "removed": [...],    # 删除的函数
            "modified": [...],   # 修改的函数 (签名或函数体变化)
            "unchanged": [...]   # 未变化的函数
        }

    def extract_public_api(self, source: str) -> list[dict]:
        """提取公开 API 清单（不以 _ 开头的函数/类）"""
        ...
```

### 3.2 Git 适配器 (`core/git_adapter.py`)

```python
class GitAdapter:
    def get_staged_files(self) -> list[str]:
        """获取暂存区中修改的 Python 文件列表"""
        # git diff --cached --name-only --diff-filter=ACM -- '*.py'

    def get_file_at_head(self, filepath: str) -> str | None:
        """获取文件在 HEAD 版本的内容"""
        # git show HEAD:<filepath>

    def get_staged_content(self, filepath: str) -> str:
        """获取文件在暂存区的内容"""
        # git show :<filepath>
```

### 3.3 LLM 调用器 (`core/llm_client.py`)

```python
class LLMClient:
    """统一的大模型调用接口，支持 Claude 和 OpenAI"""

    def __init__(self, provider: str = "claude", model: str = "claude-sonnet-4-20250514"):
        ...

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """发送请求并获取响应"""
        ...

    async def generate_test(self, function_info: FunctionInfo) -> str:
        """专用：生成测试代码"""
        ...

    async def generate_optimization(self, old_code: str, new_code: str, perf_data: dict) -> str:
        """专用：生成性能优化建议"""
        ...

    async def translate_with_context(self, text: str, context_code: str, target_langs: list[str]) -> dict:
        """专用：带上下文的翻译"""
        ...
```

### 3.4 配置文件 (`.guardian.yaml`)

```yaml
# 项目根目录的配置文件
guardian:
  # 全局开关
  enabled: true
  llm_provider: "claude"          # claude / openai
  llm_model: "claude-sonnet-4-20250514"

  # 模块开关与配置
  test_gen:
    enabled: true
    output_dir: "tests/auto_generated"
    mutation_testing: false         # 变异测试默认关闭（耗时）
    max_tests_per_function: 5

  api_diff:
    enabled: true
    strict_mode: true              # true = BREAKING 时阻断提交
    ignore_patterns:               # 忽略特定函数的 API 检查
      - "_internal_*"
      - "test_*"

  perf_guard:
    enabled: true
    threshold_warning: 0.10        # 10% 性能退化触发警告
    threshold_fail: 0.30           # 30% 性能退化阻断提交
    benchmark_timeout: 30          # 单个 benchmark 最大运行秒数

  i18n_guard:
    enabled: true
    target_langs: ["en", "ja"]
    key_style: "namespace"         # namespace (文件路径式) / flat (扁平式)
    output_format: "json"          # json / yaml
    locale_dir: "locales/"
    skip_patterns:                 # 跳过的字符串模式
      - "logger\\."
      - "# "
```

### 3.5 报告生成器 (`core/reporter.py`)

```
┌────────────────────────────────────────────────────────────────┐
│                    🛡️ AI Code Guardian 报告                     │
│                    2026-03-05 11:23:45                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  📋 扫描概况                                                    │
│  ─────────                                                     │
│  变更文件: 3 个 Python 文件                                     │
│  变更函数: 5 个（新增 2, 修改 3）                               │
│                                                                │
│  🧪 测试生成                                                    │
│  ─────────                                                     │
│  ✅ fetch_weather()  → 生成 4 个用例，全部通过                  │
│  ✅ format_report()  → 生成 3 个用例，全部通过                  │
│  ⚠️ safe_get_hourly() → 生成 3 个用例，1 个失败                │
│                                                                │
│  🔌 API 兼容性                                                  │
│  ─────────                                                     │
│  🔴 BREAKING: get_weather(city) → get_weather(city_name)       │
│  🟢 SAFE: TTLCache.clear() 新增                                │
│                                                                │
│  ⚡ 性能对比                                                    │
│  ─────────                                                     │
│  ✅ fetch_weather: 120ms → 118ms (-1.7%)                       │
│  ⚠️ format_forecast: 45ms → 58ms (+28.9%)                     │
│                                                                │
│  🌐 国际化审查                                                  │
│  ─────────                                                     │
│  📝 发现 3 处硬编码中文，已生成翻译建议                         │
│                                                                │
│  ═══════════════════════════════════════════════                │
│  总结: 1 个阻断项 (API破坏) + 2 个警告                         │
│  建议: 修复 API 兼容性后再提交                                  │
└────────────────────────────────────────────────────────────────┘
```

## 4. 目录结构

```
ai-code-guardian/
├── guardian/
│   ├── __init__.py
│   ├── cli.py                  # Click CLI 入口
│   ├── config.py               # 配置加载 (.guardian.yaml)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ast_analyzer.py     # AST 分析器
│   │   ├── git_adapter.py      # Git 操作适配
│   │   ├── llm_client.py       # LLM 统一接口
│   │   └── reporter.py         # 报告生成
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── test_gen.py         # 模块1: AI测试生成
│   │   ├── api_diff.py         # 模块2: API破坏性检测
│   │   ├── perf_guard.py       # 模块3: 性能退化守卫
│   │   └── i18n_guard.py       # 模块4: 国际化审查
│   └── templates/
│       ├── test_gen_prompt.md   # LLM Prompt 模板
│       ├── perf_opt_prompt.md
│       └── i18n_translate_prompt.md
├── tests/
│   ├── test_ast_analyzer.py
│   ├── test_api_diff.py
│   ├── test_perf_guard.py
│   └── test_i18n_guard.py
├── .guardian.yaml.example       # 配置文件示例
├── pyproject.toml
├── README.md
└── LICENSE
```

## 5. 技术栈

| 组件 | 选型 | 用途 |
|------|------|------|
| CLI 框架 | `click` | 命令行交互 |
| AST 解析 | Python 内置 `ast` | 代码结构分析 |
| Git 操作 | `gitpython` 或 subprocess | 获取 diff/staged 文件 |
| LLM 调用 | `anthropic` / `openai` SDK | AI 能力核心 |
| 测试框架 | `pytest` + `pytest-benchmark` | 测试运行与性能基准 |
| 变异测试 | `mutmut` | 测试质量评估 |
| 终端输出 | `rich` | 彩色美观的终端报告 |
| 配置管理 | `pyyaml` | 解析 `.guardian.yaml` |

## 6. 兼容性与限制

- **语言支持**：第一版仅支持 Python（AST 解析依赖 Python `ast` 模块）。
- **LLM 依赖**：需要 Claude 或 OpenAI API Key。无 Key 时，测试生成和翻译功能不可用，但 API Diff 和性能守卫仍可独立工作（纯静态分析）。
- **Git 依赖**：必须在 Git 仓库中运行。
