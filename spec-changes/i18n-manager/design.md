# 设计：多语言国际化管理器 (i18n-manager)

## 1. 架构概览 (Architecture Overview)

该工具将作为一个 Python CLI 脚本提供，核心模块分为五部分：

```
┌─────────────────────────────────────────────────────────┐
│                     CLI 入口 (cli.py)                    │
│           scan | translate | report | init               │
└──────────┬──────────┬──────────┬──────────┬──────────────┘
           │          │          │          │
     ┌─────▼────┐ ┌───▼────┐ ┌──▼───┐ ┌───▼──────┐
     │ Scanner  │ │ Dict   │ │Trans │ │ Reporter │
     │ 源码扫描 │ │ Manager│ │Engine│ │ 报告生成 │
     └──┬───┬───┘ └───┬────┘ └──┬───┘ └──────────┘
        │   │         │         │
   ┌────▼┐ ┌▼────┐    │    ┌────▼─────┐
   │Regex│ │ AST │    │    │ LLM 上下 │
   │粗筛 │ │精提取│    │    │ 文感知   │
   └─────┘ └─────┘    │    └──────────┘
                       │
              ┌────────▼────────┐
              │  语言包 (JSON)   │
              │ zh-CN / en-US   │
              └─────────────────┘
```

1. **源码扫描器 (Scanner):** 采用**两阶段提取**——正则粗筛 + AST 精提取，兼顾速度与准确性。
2. **字典管理器 (Dictionary Manager):** 管理语言包的读写、增量对比和命名空间 Key 生成。
3. **翻译引擎 (Translation Engine):** 调用外部翻译 API，LLM 模式下**携带代码上下文**进行语境翻译。
4. **报告生成器 (Reporter):** 生成翻译覆盖率报告和缺失词条清单。
5. **配置管理器 (Config Manager):** 读取并校验 `i18n.config.json`。

## 2. 详细设计 (Detailed Design)

### 2.1 两阶段扫描提取机制

#### 第一阶段：正则粗筛
快速扫描所有目标文件，提取疑似需要翻译的内容：
- 匹配中文字符：`[\u4e00-\u9fff]+`
- 匹配 i18n 调用：`\$?t\(['"](.+?)['"]\)`
- 匹配模板字符串中的中文

#### 第二阶段：AST 精提取（可选，按语言启用）
对粗筛结果所在文件进行 AST 解析，精确定位：
- **JavaScript/TypeScript:** 使用 `tree-sitter` 库解析，识别字符串字面量、模板字面量、JSX 属性值
- **Python:** 使用内置 `ast` 模块，识别字符串常量
- **Vue SFC:** 先分离 `<template>`/`<script>` 块，分别处理

```
源文件 ──┬──> 正则粗筛 ──> 候选列表
         │                     │
         └──> AST 精提取 ──> 精确列表（含上下文）
                                │
                          合并 & 去重
```

**关键优势：** AST 提取时同时捕获该词条前后 5 行代码作为"翻译上下文"，存入临时结构供 LLM 翻译使用。

### 2.2 基于文件命名空间的 Key 生成策略

摒弃纯 MD5 或纯拼音 slug 方案，采用**文件路径 + 语义摘要**的分层 Key 策略：

```
源文件路径: src/views/Login.vue
原文: "请输入密码"
→ Key: "views.login.please_enter_password"
```

生成规则：
1. 取文件相对路径，去掉 `src/` 前缀和文件扩展名，用 `.` 连接
2. 原文通过简单的拼音/英文摘要转换为 snake_case 后缀（≤40 字符）
3. 若发生冲突，自动追加数字后缀 `_2`, `_3`

```python
# 示例伪代码
def generate_key(file_path: str, text: str) -> str:
    namespace = path_to_namespace(file_path)  # "views.login"
    slug = text_to_slug(text)                 # "please_enter_password"
    return f"{namespace}.{slug}"
```

### 2.3 插值与复数处理

扫描器在提取时识别并保留动态插值标记：

| 原文格式 | 提取结果 | 说明 |
|----------|---------|------|
| `t("收到 {count} 个包裹")` | `"收到 {count} 个包裹"` | 保留 `{xxx}` 占位符 |
| `t("共 %d 条记录")` | `"共 %d 条记录"` | 保留 printf 风格占位符 |
| `` t(`你好 ${name}`) `` | `"你好 {name}"` | 模板字面量转为标准占位符 |

翻译时，指示翻译引擎**不得翻译占位符内容**，并在目标语言中保持占位符位置的语法正确性。

### 2.4 LLM 语境翻译引擎

这是本方案的**核心差异化能力**。与传统逐句翻译不同，LLM 翻译器会构造如下 Prompt：

```
你是一个专业的软件本地化翻译专家。请将以下 UI 文本从中文翻译为英文。

## 待翻译文本
"请输入密码"

## 代码上下文
该文本出现在以下代码中（src/views/Login.vue 第 42 行）：
```vue
<template>
  <div class="login-form">
    <el-input
      v-model="password"
      type="password"
      :placeholder="t('请输入密码')"
    />
    <el-button @click="handleLogin">{{ t('登录') }}</el-button>
  </div>
</template>
```

## 要求
- 这是一个密码输入框的 placeholder 文本
- 翻译应简洁、符合英文 UI 习惯
- 保留所有 {xxx} 占位符不翻译
```

**效果对比：**

| 翻译方式 | "请输入密码" | "确认" (按钮 vs 对话框) |
|----------|-------------|----------------------|
| Google Translate | "Please enter the password" | "confirm" |
| LLM 无上下文 | "Please enter your password" | "Confirm" |
| LLM 有上下文 | "Enter password" (placeholder 风格) | "OK" (按钮) / "Confirm" (对话框标题) |

### 2.5 配置管理 (`i18n.config.json`)

```json
{
  "sourceDirs": ["./src"],
  "excludeDirs": ["node_modules", "dist", "__pycache__"],
  "extensions": [".js", ".ts", ".vue", ".html", ".py"],
  "baseLanguage": "zh-CN",
  "targetLanguages": ["en-US", "ja-JP"],
  "dictionaryDir": "./locales",
  "dictionaryFormat": "nested",
  "keyStrategy": {
    "mode": "namespace",
    "stripPrefix": "src/",
    "maxSlugLength": 40
  },
  "scanner": {
    "enableAST": true,
    "contextLines": 5
  },
  "translation": {
    "engine": "llm",
    "llmProvider": "openai",
    "llmModel": "gpt-4",
    "apiKey": "${I18N_API_KEY}",
    "batchSize": 20,
    "maxConcurrency": 3,
    "retryCount": 2,
    "useCodeContext": true
  }
}
```

### 2.6 数据结构定义

语言包采用**嵌套 JSON**（可配置展平）：

```json
// locales/zh-CN.json
{
  "views": {
    "login": {
      "please_enter_password": "请输入密码",
      "login_btn": "登录",
      "received_count_packages": "收到 {count} 个包裹"
    }
  }
}

// locales/en-US.json
{
  "views": {
    "login": {
      "please_enter_password": "Enter password",
      "login_btn": "Log in",
      "received_count_packages": "Received {count} packages"
    }
  }
}
```

## 3. 错误处理与容灾 (Error Handling & Resilience)

- **AST 解析失败:** 对单个文件的 AST 解析失败不阻塞整体流程，退回到正则结果并记录警告。
- **API 失败:** 对请求报错进行重试（可配置重试次数），支持并发控制以防触发 Rate Limit。
- **并发与断点续传:** 维护一个 `.i18n-progress.json` 临时文件，记录已翻译的 key。若中断执行，下次启动仅处理未翻译完的词条。
- **Key 冲突:** 自动检测并追加数字后缀，同时在控制台输出警告供开发者审查。