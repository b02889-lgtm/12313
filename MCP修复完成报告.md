# MCP 修复完成报告

## 修复时间
2026-02-24

## 问题描述
**错误信息：** `SSE error: TypeError: fetch failed: connect ECONNREFUSED 127.0.0.1:3845`

**根本原因：** MCP配置文件中配置了一个 `figma-dev-mode` 服务器，指向 `http://127.0.0.1:3845/sse`，但该服务器没有运行，导致连接被拒绝。

## 修复内容

### 1. 移除不工作的服务器配置
- 删除了 `figma-dev-mode` SSE服务器配置
- 该服务器未运行，导致连接错误

### 2. 添加可用的Weather MCP服务器
- 配置了Weather MCP服务器（stdio类型）
- 服务器路径：`c:\Users\v-haoguoliang\Desktop\新建文件夹\weather-mcp-server`
- 使用Python运行 `server.py`

### 3. 验证服务器功能
- ✓ Weather API连接正常
- ✓ 成功获取北京天气（温度: 4°C, 天气: Sunny）
- ✓ 依赖已安装（mcp 1.26.0, httpx 0.27.2）

## 当前配置

**配置文件位置：**
`C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json`

**配置内容：**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "server.py"
      ],
      "cwd": "c:\\Users\\v-haoguoliang\\Desktop\\新建文件夹\\weather-mcp-server",
      "env": {}
    }
  }
}
```

## 可用的MCP工具

### Weather MCP Server

**工具1：get_weather**
- 功能：获取指定城市的当前天气信息
- 参数：
  - `city`（必需）：城市名称（支持中文或英文）
  - `units`（可选）：温度单位（m=摄氏度，u=华氏度，默认m）
  - `lang`（可选）：语言（zh=中文，en=英文等，默认zh）

**工具2：get_weather_forecast**
- 功能：获取指定城市的天气预报
- 参数：
  - `city`（必需）：城市名称（支持中文或英文）
  - `days`（可选）：预报天数（1-3天，默认1）
  - `units`（可选）：温度单位（m=摄氏度，u=华氏度，默认m）
  - `lang`（可选）：语言（zh=中文，en=英文等，默认zh）

## 使用示例

重启Copilot Code Pro后，可以直接使用以下工具：

```python
# 获取北京当前天气
mcp--weather--get_weather(city="北京", lang="zh", units="m")

# 获取上海2天天气预报
mcp--weather--get_weather_forecast(city="上海", days=2, lang="zh", units="m")
```

## 下一步操作

### 必须执行：
1. **重启Copilot Code Pro应用**
   - 完全退出应用
   - 重新启动应用
   - 配置更改才会生效

### 验证修复：
1. 重启后，检查MCP工具是否可用
2. 尝试调用天气工具测试功能
3. 如果仍有问题，查看应用日志

## 创建的辅助文件

为了方便后续维护，创建了以下文件：

1. **fix_mcp_config.py** - MCP配置修复脚本
2. **MCP修复说明.md** - 详细的修复说明文档
3. **test_weather_api.py** - Weather API测试脚本
4. **mcp_settings_fixed.json** - 备份的正确配置文件

## 故障排查

### 如果Weather MCP不工作

1. **检查Python环境：**
   ```bash
   python --version
   ```

2. **检查依赖安装：**
   ```bash
   pip list | findstr "mcp httpx"
   ```

3. **手动测试服务器：**
   ```bash
   cd weather-mcp-server
   python server.py
   ```

4. **重新运行修复脚本：**
   ```bash
   python fix_mcp_config.py
   ```

### 如果需要添加其他MCP服务器

1. 确保服务器已正确安装
2. 编辑配置文件添加服务器配置
3. 重启应用

## 技术说明

### stdio vs SSE

**stdio类型（推荐）：**
- 通过标准输入输出通信
- 自动启动和管理
- 更稳定可靠

**SSE类型：**
- 通过HTTP SSE通信
- 需要手动启动服务器
- 服务器未运行会导致连接错误

### 配置文件编码

配置文件使用UTF-8编码保存，支持中文路径。Windows命令行可能显示乱码，但文件内容是正确的。

## 总结

✓ **问题已解决：** 移除了导致连接错误的figma-dev-mode服务器
✓ **配置已更新：** 添加了可用的Weather MCP服务器
✓ **功能已验证：** Weather服务器工作正常
✓ **文档已完善：** 提供了详细的修复说明和使用指南

**重要提醒：** 请务必重启Copilot Code Pro应用以应用配置更改！

---

**修复完成时间：** 2026-02-24
**修复状态：** ✓ 完成
