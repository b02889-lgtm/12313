# Figma MCP 修复说明

## 修复时间
2026-02-24

## 问题描述
**错误信息：** `SSE error: TypeError: fetch failed: connect ECONNREFUSED 127.0.0.1:3845`

**根本原因：** 配置文件中使用了SSE模式（`type: "sse"`），需要手动启动服务器在端口3845上监听，但服务器未运行。

## 修复方案

### 从SSE模式改为stdio模式

**修改前（SSE模式 - 需要手动启动服务器）：**
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "type": "sse",
      "url": "http://127.0.0.1:3845/sse"
    }
  }
}
```

**修改后（stdio模式 - 自动启动）：**
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-api-key",
        "YOUR_FIGMA_API_KEY_HERE"
      ],
      "env": {}
    }
  }
}
```

### 优势对比

| 模式 | 启动方式 | 稳定性 | 推荐度 |
|------|---------|--------|--------|
| SSE | 需要手动启动服务器 | 依赖外部进程 | ⭐⭐ |
| stdio | 系统自动启动 | 更稳定可靠 | ⭐⭐⭐⭐⭐ |

## 完成配置的步骤

### 步骤1：获取Figma API Key

1. 访问 https://www.figma.com 并登录
2. 点击右上角头像 → **Settings**
3. 选择 **Account Settings**
4. 滚动到 **Personal Access Tokens**
5. 点击 **Create new token**
6. 输入描述（如：Copilot Code Pro）
7. 点击 **Create token**
8. **立即复制** token（只显示一次）

### 步骤2：更新配置文件

**方法1：使用修复脚本（推荐）**
```bash
python fix_figma_mcp.py
```

**方法2：手动编辑**
1. 打开文件：
   ```
   C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json
   ```

2. 将 `YOUR_FIGMA_API_KEY_HERE` 替换为你的真实API Key

3. 保存文件

### 步骤3：重启应用

1. 完全退出Copilot Code Pro
2. 重新启动应用

## 验证配置

重启后，Figma MCP应该自动启动。你可以通过以下方式验证：

### 检查MCP工具是否可用
在Copilot Code Pro中，应该能看到Figma相关的工具。

### 测试工具功能
尝试使用Figma工具，例如：
- "列出我的Figma文件"
- "获取文件ID为xxx的详细信息"

## 可用的Figma MCP工具

配置完成后，可以使用以下工具：

1. **获取文件信息** - 获取Figma文件的详细信息
2. **获取节点信息** - 获取特定节点的详细信息
3. **搜索文件** - 搜索Figma文件
4. **下载图片** - 下载Figma设计图片
5. **获取组件** - 获取组件信息
6. **获取样式** - 获取样式信息

## 使用示例

```python
# 获取文件列表
mcp--figma-dev-mode--list_files()

# 获取特定文件
mcp--figma-dev-mode--get_file(file_id="xxx")

# 搜索文件
mcp--figma-dev-mode--search_files(query="design")

# 下载图片
mcp--figma-dev-mode--download_images(file_id="xxx")
```

## 高级配置选项

### 使用环境变量（更安全）

1. 创建 `.env` 文件：
```env
FIGMA_API_KEY=your_actual_api_key_here
```

2. 更新配置：
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "figma-developer-mcp",
      "args": [
        "--env", "path_to_your_env_file"
      ],
      "env": {}
    }
  }
}
```

### 使用OAuth Token

如果你有OAuth Token，可以使用：
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-oauth-token", "YOUR_OAUTH_TOKEN"
      ],
      "env": {}
    }
  }
}
```

### 跳过图片下载

如果不需要图片下载功能：
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-api-key", "YOUR_API_KEY",
        "--skip-image-downloads"
      ],
      "env": {}
    }
  }
}
```

### JSON格式输出

如果需要JSON格式而非YAML：
```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "figma-developer-mcp",
      "args": [
        "--figma-api-key", "YOUR_API_KEY",
        "--json"
      ],
      "env": {}
    }
  }
}
```

## 故障排查

### 问题1：仍然显示连接错误

**原因：** API Key未替换或无效

**解决：**
1. 确认已将 `YOUR_FIGMA_API_KEY_HERE` 替换为真实API Key
2. 重新生成API Key（可能已过期）
3. 检查API Key是否有足够的权限

### 问题2：工具不可用

**原因：** 应用未重启或配置文件格式错误

**解决：**
1. 完全退出并重启Copilot Code Pro
2. 检查配置文件JSON格式是否正确
3. 查看应用日志获取详细错误信息

### 问题3：权限错误

**原因：** API Key没有访问特定文件的权限

**解决：**
1. 确认API Key有访问目标文件的权限
2. 使用OAuth Token代替Personal Access Token
3. 检查Figma团队和项目权限设置

### 问题4：速率限制

**原因：** Figma API有速率限制

**解决：**
1. 减少请求频率
2. 使用缓存避免重复请求
3. 考虑升级到Figma Professional或Organization计划

## 安全建议

1. **不要提交API Key到版本控制**
   - 使用 `.env` 文件
   - 将 `.env` 添加到 `.gitignore`

2. **定期轮换API Key**
   - 每3-6个月更换一次
   - 发现泄露立即更换

3. **使用最小权限原则**
   - 只授予必要的权限
   - 为不同项目使用不同的API Key

4. **监控API使用情况**
   - 定期检查Figma API使用统计
   - 发现异常立即调查

## 相关资源

- **Figma API文档：** https://www.figma.com/developers/api
- **figma-developer-mcp：** https://npm.im/figma-developer-mcp
- **MCP协议：** https://modelcontextprotocol.io/
- **Figma个人访问令牌：** https://www.figma.com/developers/api#access-tokens

## 总结

✓ **问题已解决：** 从SSE模式改为stdio模式
✓ **配置已更新：** 使用自动启动方式
✓ **文档已完善：** 提供详细的配置和使用指南

**下一步：**
1. 获取Figma API Key
2. 更新配置文件中的API Key
3. 重启Copilot Code Pro应用
4. 开始使用Figma MCP工具

---

**修复完成时间：** 2026-02-24
**修复状态：** ✓ 完成（等待API Key配置）
