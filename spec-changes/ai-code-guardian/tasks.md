# 任务：实现 AI Code Guardian (ai-code-guardian)

这是一个大型工具链项目。为了降低风险，我们将分阶段实施，先搭建骨架和无需 LLM 的静态分析功能，再接入大模型能力。

## 阶段 1：脚手架与核心基建 (Scaffolding & Core)

**目标**：搭建 CLI 框架，实现读取 Git 暂存区和 AST 解析的基础能力。

- [ ] **T1.1 初始化项目**：创建项目目录结构，编写 `pyproject.toml`，配置 `click`、`rich`、`pyyaml` 依赖。
- [ ] **T1.2 CLI 框架**：实现 `guardian.cli`，注册基础子命令（`check`, `test-gen`, `api-diff`, `perf`, `i18n`）。
- [ ] **T1.3 配置管理**：实现 `core.config`，支持读取 `.guardian.yaml` 并提供默认配置回退。
- [ ] **T1.4 Git 适配器**：实现 `core.git_adapter.GitAdapter`，能够可靠获取 staged 状态的 Python 文件名及其内容（HEAD 版本和 Staged 版本）。
- [ ] **T1.5 AST 分析器 (基础)**：实现 `core.ast_analyzer.ASTAnalyzer`，能从源码字符串中提取包含函数名、起止行号的 `FunctionInfo` 对象。

## 阶段 2：API 破坏性检测模块 (API Diff)
*此模块纯静态分析，不依赖 LLM，是最快能产生价值的模块。*

**目标**：实现前后版本函数签名的对比与破坏性分级。

- [ ] **T2.1 AST 签名提取**：增强 AST 分析器，精确提取函数的参数列表（名称、类型注解、默认值）和返回类型注解。
- [ ] **T2.2 对比引擎**：实现 `modules.api_diff` 中的对比逻辑，比较旧版本(HEAD)和新版本(Staged)的公开 API 签名。
- [ ] **T2.3 变更分级**：实现规则引擎，将变更分类为 SAFE（新增方法/可选参数）、WARNING（重命名参数）和 BREAKING（删除参数/改返回值）。
- [ ] **T2.4 报告输出**：集成 `rich` 库，在终端输出彩色的 API 变更报告。

## 阶段 3：国际化硬编码审查模块 (I18n Guard)
*混合模式：先做静态拦截，后加 LLM 翻译。*

**目标**：拦截代码中的魔法中文，并利用 LLM 提供翻译和替换建议。

- [ ] **T3.1 字符串节点提取**：在 AST 分析器中添加提取 `ast.Str` 和 `ast.JoinedStr`（f-string）的功能，并过滤掉 docstring 和注释。
- [ ] **T3.2 LLM 客户端基建**：实现 `core.llm_client.LLMClient`，封装对 Claude API 的调用（处理鉴权、重试、错误兜底）。
- [ ] **T3.3 翻译 Prompt 设计**：编写 `templates/i18n_translate_prompt.md`，要求 LLM 返回 JSON 格式的翻译结果。
- [ ] **T3.4 审查与交互**：实现 `modules.i18n_guard`。当发现中文字符串时，提取前后 3 行代码作为上下文发送给 LLM，并在终端提供翻译选项。

## 阶段 4：AI 测试生成模块 (TestGen)

**目标**：自动为新增或修改的无测试函数生成 pytest 单元测试。

- [ ] **T4.1 测试映射查找**：实现逻辑，判断源文件（如 `utils.py`）是否已有对应的测试文件（`test_utils.py`），并解析现有的测试函数覆盖情况。
- [ ] **T4.2 测试生成 Prompt**：编写 `templates/test_gen_prompt.md`，指导 LLM 使用 `pytest` 和 `unittest.mock` 生成测试。
- [ ] **T4.3 自动化运行验证**：将 LLM 生成的测试代码写入 `tests/auto_generated/`，并在子进程中静默运行 `pytest`。
- [ ] **T4.4 结果过滤**：收集 pytest 执行结果。如果测试通过，则正式保留；如果失败，则抛出警告或请求 LLM 进行自我修正（上限 1 次）。

## 阶段 5：性能退化守卫 (PerfGuard)
*最复杂的模块，需要本地运行基准测试。*

**目标**：检测代码修改是否导致执行时间显著增加。

- [ ] **T5.1 依赖集成**：在项目中引入 `pytest-benchmark`。
- [ ] **T5.2 哑测试生成**：如果变更函数没有 benchmark 测试，调用 LLM 极速生成一个“仅包含有效输入参数”的极简 benchmark 运行器。
- [ ] **T5.3 隔离执行**：在安全的临时目录中，分别加载 HEAD 版本和 Staged 版本的代码，运行 benchmark，收集执行时间。
- [ ] **T5.4 退化分析与建议**：对比耗时差异。若退化超过阈值（如 30%），截取新旧代码发送给 LLM，请求 `templates/perf_opt_prompt.md` 给出优化建议。

## 阶段 6：整合与交付 (Integration)

**目标**：将所有模块组装成预提交钩子，并提供完整的报告。

- [ ] **T6.1 统一编排**：完善 `guardian check` 命令，通过多线程或 `asyncio` 并发执行 TestGen、APIDiff、PerfGuard 和 I18nGuard（注意依赖顺序或解耦）。
- [ ] **T6.2 综合报告生成**：实现 `core.reporter`，将四个模块的独立结果汇总为一个美观的终端仪表盘 (Dashboard)。
- [ ] **T6.3 Pre-commit Hook 安装器**：实现 `guardian install-hook`，自动在当前 Git 仓库的 `.git/hooks/pre-commit` 中写入触发脚本。
- [ ] **T6.4 文档编写**：更新 `README.md`，提供快速开始指南、配置项说明和所有命令的帮助文档。

