## 上下文

`custom-tools-mcp/README.md` 当前描述了 8 个工具（text_transform、hash_generator 等），但 `server.py` 的 `list_tools()` 只注册了一个 `run_python_snippet` 工具。这个工具是一个沙箱化的 Python 代码执行器，具有 AST 安全检查和模块黑名单机制。

README 内容可能来自早期设计阶段，而代码后来改为单一通用工具方案。文档从未更新。

## 目标 / 非目标

**目标：**

- 重写 README 使工具描述与 server.py 完全一致
- 准确描述 `run_python_snippet` 的功能、参数、安全限制
- 提供基于实际代码的使用示例
- 保留有用的部分（安装说明、MCP 配置、架构图）

**非目标：**

- 不修改 server.py 代码
- 不添加 README 中曾列出的那 8 个工具
- 不改变项目架构或依赖

## 决策

1. **README 结构**：采用以下章节顺序
   - 标题和简介
   - 提供的工具（只有 `run_python_snippet`）
   - 安全机制说明（从 server.py 提取的黑名单列表）
   - 安装与运行（保留原有内容）
   - 使用示例（重写为实际参数格式）
   - 技术架构（保留但更新）

2. **示例风格**：使用 JSON 输入 + Markdown 输出的格式，与实际 MCP 调用一致

3. **安全信息来源**：直接从 `server.py` 的 `BLOCKED_NAMES`、`BLOCKED_MODULES` 和 `safe_globals` 常量提取，确保文档与代码同步

## 风险 / 权衡

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 旧 README 中某些工具描述可能是未来计划 | 低 | proposal 中已说明这是文档修正而非功能删除 |
| 安全限制列表可能随代码变更过时 | 中 | 在 README 中注明"以代码为准" |
| 删除大量内容可能丢失有用信息 | 低 | "如何添加新工具"章节保留 |
