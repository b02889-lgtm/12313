#!/usr/bin/env node
const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { z } = require("zod");

// 创建 MCP 服务器
const server = new McpServer({
  name: "demo-resources-server",
  version: "1.0.0"
});

// 示例文档数据
const documents = {
  "welcome": {
    title: "欢迎使用文档资源服务器",
    content: `# 欢迎使用文档资源服务器

这是一个演示 MCP Resources 功能的示例服务器。

## 什么是 MCP Resources？

Resources（资源）是 MCP 协议中的核心概念之一，用于向 AI 助手提供只读的数据内容。

## 本服务器提供的资源

1. **欢迎文档** - 您正在阅读的文档
2. **开发指南** - 开发者使用指南
3. **API 参考** - API 文档参考

## 如何使用

您可以通过访问特定的 URI 来获取这些资源：
- doc://welcome
- doc://guide
- doc://api

创建时间: ${new Date().toISOString()}
`
  },
  "guide": {
    title: "开发者指南",
    content: `# 开发者指南

## 快速开始

1. 安装依赖
   \`\`\`bash
   npm install @modelcontextprotocol/sdk zod
   \`\`\`

2. 创建服务器
   \`\`\`javascript
   const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
   const server = new McpServer({
     name: "my-server",
     version: "1.0.0"
   });
   \`\`\`

3. 添加资源
   \`\`\`javascript
   server.resource(
     "my-resource",
     { uri: "doc://example", list: true },
     async (uri) => {
       return {
         contents: [{
           uri: uri.href,
           mimeType: "text/markdown",
           text: "Hello, World!"
         }]
       };
     }
   );
   \`\`\`

## 最佳实践

- 使用清晰的 URI 命名
- 提供适当的 MIME 类型
- 保持资源内容简洁
- 添加时间戳以便追踪更新

更新时间: ${new Date().toISOString()}
`
  },
  "api": {
    title: "API 参考",
    content: `# API 参考

## 资源 API

### server.resource(name, uri, handler)

注册一个静态资源。

**参数:**
- \`name\` (string): 资源名称
- \`uri\` (object): URI 配置对象
  - \`uri\` (string): 资源的 URI
  - \`list\` (boolean): 是否在资源列表中显示
- \`handler\` (function): 资源处理函数

**返回值:** 无

### server.resource(name, template, handler)

注册一个动态资源模板。

**参数:**
- \`name\` (string): 资源名称
- \`template\` (ResourceTemplate): 资源模板对象
- \`handler\` (function): 资源处理函数

**示例:**
\`\`\`javascript
server.resource(
  "dynamic-doc",
  new ResourceTemplate("doc://{id}", { list: true }),
  async (uri, { id }) => {
    return {
      contents: [{
        uri: uri.href,
        mimeType: "text/markdown",
        text: \`Document ID: \${id}\`
      }]
    };
  }
);
\`\`\`

## 工具 API

### server.tool(name, schema, handler)

注册一个工具。

**参数:**
- \`name\` (string): 工具名称
- \`schema\` (object): Zod 验证模式
- \`handler\` (function): 工具处理函数

文档版本: 1.0.0
最后更新: ${new Date().toISOString()}
`
  }
};

// 添加一个工具 - 获取特定文档
server.tool(
  "get_document",
  {
    id: z.enum(["welcome", "guide", "api"]).describe("文档ID")
  },
  async ({ id }) => {
    const doc = documents[id];
    if (!doc) {
      return {
        content: [{
          type: "text",
          text: `错误: 找不到文档 "${id}"`
        }],
        isError: true
      };
    }

    return {
      content: [{
        type: "text",
        text: doc.content
      }]
    };
  }
);

// 添加一个工具 - 列出所有可用文档
server.tool(
  "list_documents",
  {
    format: z.enum(["json", "markdown"]).optional().describe("输出格式")
  },
  async ({ format = "json" }) => {
    const docList = Object.entries(documents).map(([id, doc]) => ({
      id,
      title: doc.title,
      uri: `doc://${id}`
    }));

    if (format === "json") {
      return {
        content: [{
          type: "text",
          text: JSON.stringify(docList, null, 2)
        }]
      };
    } else {
      const markdown = docList.map(doc =>
        `- **${doc.title}** (\`${doc.uri}\`)`
      ).join("\n");

      return {
        content: [{
          type: "text",
          text: `# 可用文档列表\n\n${markdown}`
        }]
      };
    }
  }
);

// 添加一个工具 - 搜索文档
server.tool(
  "search_documents",
  {
    query: z.string().describe("搜索关键词")
  },
  async ({ query }) => {
    const results = Object.entries(documents)
      .filter(([id, doc]) => {
        const content = doc.content.toLowerCase();
        return content.includes(query.toLowerCase());
      })
      .map(([id, doc]) => ({
        id,
        title: doc.title,
        uri: `doc://${id}`
      }));

    return {
      content: [{
        type: "text",
        text: JSON.stringify(results, null, 2)
      }]
    };
  }
);

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Demo Resources MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
