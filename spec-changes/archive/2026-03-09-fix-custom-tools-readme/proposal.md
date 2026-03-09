## 为什么

`custom-tools-mcp` 项目的 README.md 存在严重的**文档与代码不一致**问题：

- README 声称提供 8 个独立工具（text_transform、hash_generator、base64_codec 等）
- 实际代码（server.py）只实现了 1 个工具：`run_python_snippet`（通用 Python 代码片段执行器）

这会导致用户（包括 AI 助手）产生错误预期，尝试调用不存在的工具。同时，README 中的使用示例与实际工具参数格式不匹配，进一步加深了困惑。

## 变更内容

重写 `custom-tools-mcp/README.md`，使其准确反映 server.py 的真实能力：

- 修正工具列表：只有 `run_python_snippet` 一个工具
- 更新使用示例：展示实际的 code 参数和输出格式
- 说明安全机制：AST 静态检查、模块黑名单、函数黑名单
- 列出预注入的安全标准库：math、random、json、re、datetime 等

## 功能 (Capabilities)

### 新增功能

无（纯文档修正）

### 修改功能

- `custom-tools-readme`: 修正 README.md 使其与实际代码一致

## 影响

- 修改文件：`custom-tools-mcp/README.md`
- 无代码变更、无依赖变更、无 API 变更
- 影响范围：仅文档层面，但修正了关键的功能描述错误
