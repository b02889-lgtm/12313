# Figma MCP 安装完成

## ✅ 安装状态

**包名：** `figma-developer-mcp`
**版本：** 0.6.4
**安装位置：** 全局安装

---

## 🚀 使用方法

### 1. 获取 Figma API Key

1. 登录 [Figma](https://www.figma.com)
2. 进入 **Settings** → **Account Settings**
3. 滚动到 **Personal Access Tokens**
4. 点击 **Create new token**
5. 复制生成的 token

### 2. 启动 Figma MCP 服务器

#### 方式一：使用命令行参数

```bash
figma-developer-mcp --figma-api-key YOUR_API_KEY
```

#### 方式二：使用环境变量

创建 `.env` 文件：

```env
FIGMA_API_KEY=your_api_key_here
```

然后运行：

```bash
figma-developer-mcp --env .env
```

#### 方式三：使用 OAuth Token

```bash
figma-developer-mcp --figma-oauth-token YOUR_OAUTH_TOKEN
```

---

## ⚙️ 配置选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--figma-api-key` | Figma API 密钥 | - |
| `--figma-oauth-token` | Figma OAuth 令牌 | - |
| `--env` | 自定义 .env 文件路径 | - |
| `--port` | 服务器端口 | - |
| `--json` | 输出 JSON 格式（默认 YAML） | `false` |
| `--skip-image-downloads` | 跳过图片下载工具 | `false` |

---

## 📋 可用工具

安装后，Figma MCP 提供以下工具：

1. **获取文件信息** - 获取 Figma 文件的详细信息
2. **获取节点信息** - 获取特定节点的详细信息
3. **搜索文件** - 搜索 Figma 文件
4. **下载图片** - 下载 Figma 设计图片
5. **获取组件** - 获取组件信息
6. **获取样式** - 获取样式信息

---

## 🔧 在 Claude Desktop 中配置

编辑 Claude Desktop 配置文件：

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "figma": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-api-key", "YOUR_API_KEY_HERE"
      ]
    }
  }
}
```

---

## 📖 使用示例

### 获取文件列表

```
请列出我所有的 Figma 文件
```

### 获取特定文件

```
请获取文件 ID 为 xxx 的详细信息
```

### 下载设计图片

```
请下载这个设计的图片
```

### 分析设计

```
请分析这个 Figma 设计的布局和组件
```

---

## 🌐 相关链接

- **Figma API 文档：** https://www.figma.com/developers/api
- **figma-developer-mcp：** https://npm.im/figma-developer-mcp
- **MCP 协议：** https://modelcontextprotocol.io/

---

## ⚠️ 注意事项

1. **API Key 安全** - 不要将 API Key 提交到版本控制
2. **权限限制** - API Key 只能访问你有权限的文件
3. **速率限制** - Figma API 有速率限制，请合理使用
4. **OAuth vs PAT** - OAuth Token 适用于团队协作，PAT 适用于个人使用

---

## 🎯 快速开始

```bash
# 1. 设置环境变量
set FIGMA_API_KEY=your_api_key_here

# 2. 启动服务器
figma-developer-mcp --figma-api-key %FIGMA_API_KEY%

# 3. 在 Claude 中使用
# 直接询问关于 Figma 文件的问题
```

---

**安装时间：** 2026-02-05
**Node.js 版本：** v24.11.0
