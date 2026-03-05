# 任务：多语言国际化管理器 (i18n-manager)

## 实现任务清单

### 阶段 1：项目初始化与基础设施
- [ ] **T1.1** 创建项目目录结构 `i18n-manager/`，初始化 `pyproject.toml`，添加 `requirements.txt`（含 `tree-sitter`, `click`, `openai`, `googletrans`, `pypinyin` 等依赖）
- [ ] **T1.2** 创建配置文件模块 `config.py`，支持读取并校验 `i18n.config.json` 配置（含 `keyStrategy`, `scanner`, `translation` 等新增字段）
- [ ] **T1.3** 创建 CLI 入口 `cli.py`，使用 `click` 注册子命令（`init`, `scan`, `translate`, `report`）
- [ ] **T1.4** 创建 `i18n.config.json` 配置模板文件，含完整的默认值注释

### 阶段 2：源码扫描器 (Scanner) - 两阶段提取
- [ ] **T2.1** 实现文件遍历器，根据配置中的 `sourceDirs`、`excludeDirs`、`extensions` 过滤目标文件
- [ ] **T2.2** 实现正则粗筛模块，匹配中文字符串（`[\u4e00-\u9fff]`）及 `t('...')`、`$t('...')`、模板字符串中的中文等调用模式
- [ ] **T2.3** 实现插值识别模块，支持识别并保留 `{xxx}`、`%d`、`%s`、`${xxx}` 等占位符格式
- [ ] **T2.4** 实现 AST 精提取模块（JS/TS），使用 `tree-sitter` 解析字符串字面量、模板字面量、JSX 属性值
- [ ] **T2.5** 实现 AST 精提取模块（Python），使用内置 `ast` 模块解析字符串常量
- [ ] **T2.6** 实现代码上下文捕获器，在 AST 提取时同时保存词条前后 N 行代码（可配置，默认 5 行）
- [ ] **T2.7** 实现两阶段结果的合并去重逻辑（正则结果 ∪ AST 结果，以 AST 为准去重）
- [ ] **T2.8** 编写扫描器的单元测试（含边界情况：嵌套引号、多行字符串、JSX 混合等）

### 阶段 3：Key 生成与字典管理器 (Dictionary Manager)
- [ ] **T3.1** 实现文件路径命名空间转换器（`src/views/Login.vue` → `views.login`），支持配置 `stripPrefix`
- [ ] **T3.2** 实现原文 → slug 转换器（使用 `pypinyin` 将中文转为拼音 snake_case，限制最大长度）
- [ ] **T3.3** 实现 Key 生成器（组合命名空间 + slug），含冲突检测与自动编号后缀
- [ ] **T3.4** 实现语言包读取器，支持加载嵌套和展平两种格式的 JSON 语言文件
- [ ] **T3.5** 实现增量对比逻辑：对比扫描结果与已有基础语言包，找出新增的 key
- [ ] **T3.6** 实现缺失检查逻辑：对比基础语言包与所有目标语言包，找出未翻译的 key
- [ ] **T3.7** 实现语言包回写功能，保持 JSON 格式化输出、嵌套层级和 key 按字母排序
- [ ] **T3.8** 编写字典管理器的单元测试（含 Key 冲突、嵌套/展平格式转换等）

### 阶段 4：翻译引擎 (Translation Engine) - LLM 语境翻译
- [ ] **T4.1** 定义翻译引擎抽象接口 `BaseTranslator`（含 `translate(text, src, dest, context=None)` 方法）
- [ ] **T4.2** 实现 Google Translate 翻译器（通过 `googletrans` 或官方 API，作为基础翻译后备）
- [ ] **T4.3** 实现 LLM 语境翻译器（通过 OpenAI API），核心功能：
  - 构造含代码上下文的 Prompt（包括文件路径、行号、前后代码片段）
  - 指示 LLM 不翻译 `{xxx}` 等占位符
  - 根据 UI 元素类型（按钮/placeholder/标题等）调整翻译风格
- [ ] **T4.4** 实现批量翻译与并发控制（使用 `asyncio`，支持可配置的 `maxConcurrency` 和 `batchSize`）
- [ ] **T4.5** 实现断点续传逻辑：维护 `.i18n-progress.json` 临时文件，记录已完成的翻译 key
- [ ] **T4.6** 实现翻译失败重试机制（可配置重试次数和退避策略）
- [ ] **T4.7** 编写翻译引擎的单元测试（含 mock 外部 API、占位符保留验证、上下文 Prompt 构造验证）

### 阶段 5：输出与报告
- [ ] **T5.1** 实现翻译覆盖率报告生成：
  - 各语言的翻译完成百分比
  - 缺失 key 列表（按命名空间分组）
  - 含占位符的词条统计
- [ ] **T5.2** 实现 `scan` 命令的格式化输出（发现的新文本摘要、按文件分组、高亮插值变量）
- [ ] **T5.3** 实现 `translate` 命令的执行进度条和结果摘要（成功/失败/跳过数量）
- [ ] **T5.4** 实现 `init` 命令，在项目中生成默认的 `i18n.config.json` 和 `locales/` 目录

### 阶段 6：集成测试与文档
- [ ] **T6.1** 创建示例项目目录 `tests/fixtures/sample-project/`，包含 JS/TS/Vue/Python 混合源码
- [ ] **T6.2** 编写端到端集成测试：验证 `scan → translate → report` 完整工作流
- [ ] **T6.3** 编写 `README.md`，包含：
  - 安装说明与依赖要求
  - 快速入门（3 分钟上手）
  - 配置说明（所有字段详解）
  - CLI 命令用法示例
  - LLM 语境翻译的效果对比展示
- [ ] **T6.4** 编写 `CHANGELOG.md` 初始版本记录