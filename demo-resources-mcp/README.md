# 📄 MCP 资源演示服务器 (demo-resources-mcp)

一个基于 Node.js 的 MCP 资源演示服务器，展示如何使用 Model Context Protocol 提供文档资源和工具。通过 3 个内置工具和 3 份示例文档，帮助开发者快速理解 MCP Resources 的工作方式。

## ✨ 功能特性

- 📚 **文档资源服务** — 提供 3 份结构化内置文档（欢迎、开发指南、API 参考）
- 🔧 **3 个查询工具** — 获取文档、列出文档、搜索文档
- 📝 **多格式输出** — 支持 JSON 和 Markdown 两种输出格式
- 🔍 **全文搜索** — 按关键词在文档内容中搜索
- 🚀 **零配置启动** — 无需 API 密钥，即装即用

## 📦 安装步骤

确保已安装 Node.js 16+，然后安装依赖：

```bash
cd demo-resources-mcp
npm install
```

依赖清单：
- `@modelcontextprotocol/sdk` ^1.27.0 — MCP 协议 SDK
- `zod` ^4.3.6 — 参数验证库

## ⚙️ MCP 客户端配置

将以下配置添加到你的 MCP 客户端配置文件中：

```json
{
  "mcpServers": {
    "demo-resources": {
      "command": "node",
      "args": ["index.js"],
      "cwd": "c:/Users/v-haoguoliang/Desktop/新建文件夹/demo-resources-mcp"
    }
  }
}
```

> **注意**：请将 `cwd` 路径修改为你实际的 `demo-resources-mcp` 目录路径。

## 🔧 可用工具

### 1. `get_document` — 获取指定文档

按文档 ID 获取完整内容。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | enum | ✅ | 文档 ID，可选值：`welcome`、`guide`、`api` |

**调用示例**：
```json
{
  "id": "welcome"
}
```

**返回**：对应文档的 Markdown 格式全文。

---

### 2. `list_documents` — 列出所有文档

获取所有可用文档的列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `format` | enum | ❌ | 输出格式：`json`（默认）或 `markdown` |

**调用示例（JSON 格式）**：
```json
{
  "format": "json"
}
```

**返回示例**：
```json
[
  { "id": "welcome", "title": "欢迎使用文档资源服务器", "uri": "doc://welcome" },
  { "id": "guide", "title": "开发者指南", "uri": "doc://guide" },
  { "id": "api", "title": "API 参考", "uri": "doc://api" }
]
```

---

### 3. `search_documents` — 搜索文档

按关键词在所有文档内容中进行全文搜索（不区分大小写）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |

**调用示例**：
```json
{
  "query": "资源"
}
```

**返回**：匹配的文档列表（JSON 格式，包含 id、title、uri）。

## 📚 内置文档资源

服务器内置 3 份演示文档，通过 `doc://` URI 协议访问：

| 文档 ID | URI | 标题 | 内容概述 |
|---------|-----|------|----------|
| `welcome` | `doc://welcome` | 欢迎使用文档资源服务器 | MCP Resources 概念介绍、服务器功能说明 |
| `guide` | `doc://guide` | 开发者指南 | 快速开始教程、代码示例、最佳实践 |
| `api` | `doc://api` | API 参考 | server.resource() 和 server.tool() 的 API 文档 |

## 💡 使用示例

在支持 MCP 的 AI 助手中，你可以这样使用：

```
# 获取欢迎文档
请获取 welcome 文档的内容

# 查看所有文档列表（Markdown 格式）
请以 markdown 格式列出所有可用文档

# 搜索包含"快速开始"的文档
请搜索关键词"快速开始"
```

## 🏗️ 技术架构

```
┌─────────────────┐    stdio     ┌──────────────────────┐
│  MCP 客户端      │◄───────────►│  demo-resources-mcp  │
│  (AI 助手)       │             │                      │
└─────────────────┘             │  ┌────────────────┐   │
                                │  │ 工具层          │   │
                                │  │ get_document    │   │
                                │  │ list_documents  │   │
                                │  │ search_documents│   │
                                │  └───────┬────────┘   │
                                │          │             │
                                │  ┌───────▼────────┐   │
                                │  │ 数据层          │   │
                                │  │ documents = {   │   │
                                │  │   welcome: ..., │   │
                                │  │   guide: ...,   │   │
                                │  │   api: ...      │   │
                                │  │ }               │   │
                                │  └────────────────┘   │
                                └──────────────────────┘
```

**技术栈**：
- **运行时**：Node.js 16+
- **MCP SDK**：@modelcontextprotocol/sdk ^1.27.0
- **参数验证**：zod ^4.3.6
- **传输方式**：StdioServerTransport
- **模块系统**：CommonJS

## 📄 许可证

MIT License
