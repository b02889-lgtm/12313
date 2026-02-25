# MCP 服务未显示问题诊断指南

## 🔍 问题现象

在 Claude Desktop 的 MCP 服务市场中看不到已安装的 Figma MCP 服务。

---

## ✅ 已确认的状态

### 1. Figma MCP 已安装
```bash
C:\Users\v-haoguoliang\AppData\Roaming\npm\figma-developer-mcp
C:\Users\v-haoguoliang\AppData\Roaming\npm\figma-developer-mcp.cmd
```

### 2. 配置文件已创建
位置：`C:\Users\v-haoguoliang\AppData\Roaming\Claude\claude_desktop_config.json`

内容：
```json
{
  "mcpServers": {
    "figma": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-api-key", "YOUR_FIGMA_API_KEY_HERE"
      ]
    }
  }
}
```

---

## ⚠️ 可能的问题

### 问题 1: API Key 未替换 ⚠️ **最可能的原因**

配置文件中的 API Key 还是占位符：
```json
"--figma-api-key", "YOUR_FIGMA_API_KEY_HERE"
```

**解决方案：**

1. 获取 Figma API Key：
   - 登录 [Figma](https://www.figma.com)
   - 进入 **Settings** → **Account Settings**
   - 滚动到 **Personal Access Tokens**
   - 点击 **Create new token** 并复制

2. 编辑配置文件：
   - 打开：`C:\Users\v-haoguoliang\AppData\Roaming\Claude\claude_desktop_config.json`
   - 将 `YOUR_FIGMA_API_KEY_HERE` 替换为您的真实 API Key
   - 保存文件

3. 重启 Claude Desktop

---

### 问题 2: Claude Desktop 未重启

配置文件修改后，**必须完全重启** Claude Desktop 才能生效。

**解决方案：**
1. 完全退出 Claude Desktop（确保后台进程也关闭）
2. 重新启动 Claude Desktop

---

### 问题 3: 配置文件格式错误

JSON 格式必须正确，不能有语法错误。

**检查方法：**
- 使用 JSON 验证工具检查格式
- 确保所有引号、逗号、括号都正确

---

### 问题 4: MCP 服务启动失败

如果配置正确但服务仍不显示，可能是服务启动失败。

**检查方法：**

1. 手动测试 MCP 服务：
```bash
figma-developer-mcp --figma-api-key YOUR_API_KEY
```

2. 查看错误信息：
- 如果显示错误，记录错误信息
- 检查 API Key 是否有效
- 检查网络连接

---

## 🔧 完整配置步骤

### 步骤 1: 获取 Figma API Key

1. 访问 https://www.figma.com
2. 登录账户
3. 点击右上角头像 → **Settings**
4. 选择 **Account Settings**
5. 滚动到 **Personal Access Tokens**
6. 点击 **Create new token**
7. 输入描述（如：Claude Desktop）
8. 点击 **Create token**
9. **立即复制** token（只显示一次）

### 步骤 2: 更新配置文件

1. 打开文件：
   ```
   C:\Users\v-haoguoliang\AppData\Roaming\Claude\claude_desktop_config.json
   ```

2. 替换为以下内容（使用您的真实 API Key）：
   ```json
   {
     "mcpServers": {
       "figma": {
         "command": "figma-developer-mcp",
         "args": [
           "--figma-api-key", "您的真实API_KEY"
         ]
       }
     }
   }
   ```

3. 保存文件

### 步骤 3: 重启 Claude Desktop

1. 完全退出 Claude Desktop
2. 确保后台进程已关闭
3. 重新启动 Claude Desktop

### 步骤 4: 验证服务

1. 打开 Claude Desktop
2. 查看设置中的 MCP 服务列表
3. 应该能看到 "figma" 服务

---

## 📋 验证清单

- [ ] Figma API Key 已获取
- [ ] 配置文件中的 API Key 已替换
- [ ] 配置文件格式正确（JSON 有效）
- [ ] Claude Desktop 已完全重启
- [ ] 网络连接正常
- [ ] API Key 有效（未过期）

---

## 🆘 仍然无法显示？

### 检查 Claude Desktop 日志

1. 打开 Claude Desktop
2. 按 `Ctrl + Shift + I` 打开开发者工具
3. 查看 Console 标签页
4. 查找与 MCP 相关的错误信息

### 检查系统日志

1. 打开 Windows 事件查看器
2. 查看 Windows 日志 → 应用程序
3. 查找 Claude Desktop 相关的错误

### 尝试其他 MCP 服务

测试其他 MCP 服务是否能正常工作：
- GitHub MCP
- Google Drive MCP
- Slack MCP

如果其他服务也不显示，可能是 Claude Desktop 本身的问题。

---

## 📞 获取帮助

如果以上方法都无法解决问题：

1. **查看官方文档：**
   - Claude Desktop 文档
   - MCP 协议文档

2. **提交问题：**
   - Claude Desktop GitHub Issues
   - Figma MCP GitHub Issues

3. **社区支持：**
   - Claude Discord 社区
   - Stack Overflow

---

## 📝 常见错误

### 错误 1: "Invalid API Key"
**原因：** API Key 无效或已过期
**解决：** 重新生成 API Key

### 错误 2: "Connection refused"
**原因：** 网络连接问题
**解决：** 检查网络连接和防火墙设置

### 错误 3: "Command not found"
**原因：** figma-developer-mcp 未正确安装
**解决：** 重新安装：`npm install -g figma-developer-mcp`

### 错误 4: "Permission denied"
**原因：** 配置文件权限问题
**解决：** 以管理员身份运行 Claude Desktop

---

## 🎯 快速修复命令

```bash
# 1. 重新安装 Figma MCP
npm install -g figma-developer-mcp

# 2. 验证安装
where figma-developer-mcp

# 3. 测试服务（替换 YOUR_API_KEY）
figma-developer-mcp --figma-api-key YOUR_API_KEY --help

# 4. 检查配置文件
type %APPDATA%\Claude\claude_desktop_config.json
```

---

## 💡 最佳实践

### 1. API Key 管理
- **不要将 API Key 提交到版本控制系统**
- 使用环境变量存储敏感信息
- 定期轮换 API Key 以提高安全性
- 为不同的项目使用不同的 API Key

### 2. 配置文件备份
```bash
# 备份配置文件
copy %APPDATA%\Claude\claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json.backup
```

### 3. 多 MCP 服务配置
如果需要配置多个 MCP 服务，可以在配置文件中添加多个服务：

```json
{
  "mcpServers": {
    "figma": {
      "command": "figma-developer-mcp",
      "args": ["--figma-api-key", "YOUR_FIGMA_API_KEY"]
    },
    "github": {
      "command": "mcp-server-github",
      "args": ["--github-token", "YOUR_GITHUB_TOKEN"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\YourName\\Documents"]
    }
  }
}
```

### 4. 性能优化建议
- 只启用需要的 MCP 服务，避免资源浪费
- 定期清理不使用的 MCP 服务配置
- 监控 MCP 服务的资源使用情况

### 5. 故障排查流程
1. 检查配置文件格式是否正确
2. 验证 API Key 是否有效
3. 测试 MCP 服务是否能独立运行
4. 查看 Claude Desktop 日志
5. 尝试重启应用

---

## 🚀 高级配置选项

### 1. 环境变量配置
对于更安全的配置管理，可以使用环境变量：

```json
{
  "mcpServers": {
    "figma": {
      "command": "figma-developer-mcp",
      "args": ["--figma-api-key", "${FIGMA_API_KEY}"]
    }
  }
}
```

然后在系统环境变量中设置 `FIGMA_API_KEY`。

### 2. 自定义 MCP 服务端口
某些 MCP 服务支持自定义端口：

```bash
figma-developer-mcp --port 3001 --figma-api-key YOUR_API_KEY
```

在配置文件中指定端口：
```json
{
  "mcpServers": {
    "figma": {
      "command": "figma-developer-mcp",
      "args": [
        "--port", "3001",
        "--figma-api-key", "YOUR_API_KEY"
      ]
    }
  }
}
```

### 3. 日志级别配置
为 MCP 服务设置不同的日志级别以获取更多调试信息：

```bash
figma-developer-mcp --log-level debug --figma-api-key YOUR_API_KEY
```

### 4. 代理配置
如果需要通过代理访问网络，可以设置环境变量：

```bash
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=https://proxy.company.com:8080
figma-developer-mcp --figma-api-key YOUR_API_KEY
```

---

**创建时间：** 2026-02-05
**最后更新：** 2026-02-05
