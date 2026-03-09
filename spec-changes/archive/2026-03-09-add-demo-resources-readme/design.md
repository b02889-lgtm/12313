# 设计：为 demo-resources-mcp 添加 README.md

## 上下文

`demo-resources-mcp` 是一个基于 Node.js 的 MCP 资源演示服务器。它使用 `@modelcontextprotocol/sdk` (v1.27.0) 和 `zod` (v4.3.6)，通过 stdio 传输提供 3 个工具和 3 份内置文档资源。当前项目缺少 README.md。

### 代码分析结果

- **入口文件**: `index.js` (248 行)
- **3 个工具**:
  - `get_document(id)` — 按 ID 获取文档，id 为枚举：welcome/guide/api
  - `list_documents(format?)` — 列出所有文档，支持 json/markdown 格式
  - `search_documents(query)` — 按关键词搜索文档内容
- **3 份内置文档**: welcome（欢迎页）、guide（开发指南）、api（API 参考）
- **URI 模式**: `doc://welcome`、`doc://guide`、`doc://api`
- **传输方式**: StdioServerTransport

## 目标 / 非目标

**目标：**
- 创建清晰、完整的 README.md，使新用户能在 5 分钟内理解并使用该服务
- 准确描述 3 个工具的参数和返回值
- 提供可直接使用的 MCP 客户端配置
- 保持与其他 MCP 项目 README 风格一致

**非目标：**
- 不修改 index.js 代码
- 不修改 package.json
- 不添加新功能

## 决策

### README 章节结构

```
1. 标题 + 简介
2. ✨ 功能特性（要点列表）
3. 📦 安装步骤（npm install）
4. ⚙️ MCP 配置（JSON 示例）
5. 🔧 可用工具（3 个工具详细说明）
6. 📚 内置文档资源（3 个资源的 URI 和描述）
7. 💡 使用示例（每个工具一个调用示例）
8. 🏗️ 技术架构（ASCII 图）
9. 许可证
```

### 风格决策

- 使用 emoji 前缀标记章节（与 weather-mcp-server README 风格一致）
- 工具参数使用表格展示（参数名/类型/必填/说明）
- 配置示例使用当前工作区实际路径
- 使用 ASCII 架构图展示 MCP 通信流程

## 风险 / 权衡

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 路径硬编码 | 其他用户需修改路径 | 在配置中添加提醒注释 |
| package.json description 为空 | 与 README 不一致 | 本次不修改，后续可处理 |
