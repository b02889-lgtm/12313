# MCP 修复说明

## 问题描述

**错误信息：** `SSE error: TypeError: fetch failed: connect ECONNREFUSED 127.0.0.1:3845`

**原因：** MCP配置文件中配置了一个 `figma-dev-mode` 服务器，指向 `http://127.0.0.1:3845/sse`，但该服务器没有运行，导致连接被拒绝。

## 修复内容

### 1. 更新MCP配置文件

**文件位置：** `C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json`

**修改前：**
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

**修改后：**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "server.py"
      ],
      "cwd": "c:/Users/v-haoguoliang/Desktop/新建文件夹/weather-mcp-server",
      "env": {}
    }
  }
}
```

### 2. 验证Weather MCP服务器

**服务器位置：** `weather-mcp-server/server.py`

**已安装的依赖：**
- mcp 1.26.0
- httpx 0.27.2
- httpx-sse 0.4.3

**可用工具：**
1. `get_weather` - 获取指定城市的当前天气信息
2. `get_weather_forecast` - 获取指定城市的天气预报

**测试结果：**
- ✓ Weather API连接正常
- ✓ 成功获取北京天气（温度: 4°C, 天气: Sunny）
- ✓ 服务器配置正确

## 使用说明

### 重启应用

修改配置文件后，需要重启Copilot Code Pro应用才能生效：

1. 完全退出Copilot Code Pro
2. 重新启动应用

### 使用Weather MCP工具

重启后，可以使用以下工具：

#### 获取当前天气
```python
# 工具会自动调用，例如：
mcp--weather--get_weather(
    city="北京",
    lang="zh",
    units="m"
)
```

#### 获取天气预报
```python
# 工具会自动调用，例如：
mcp--weather--get_weather_forecast(
    city="上海",
    days=2,
    lang="zh",
    units="m"
)
```

## 可用的MCP服务器

### 1. Weather MCP Server（已配置）

**类型：** stdio（标准输入输出）

**功能：**
- 获取全球城市当前天气
- 获取1-3天天气预报
- 支持多种语言（中文、英文、日文、法文、德文）
- 支持公制和美制温度单位

**数据源：** wttr.in API

### 2. MCP Streaming Server（可选）

**位置：** `mcp-streaming-server/server.py`

**类型：** HTTP/SSE

**功能：**
- 流式文本生成
- 流式数字序列生成
- 流式进度报告

**如需启用，可以添加到配置文件：**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "c:/Users/v-haoguoliang/Desktop/新建文件夹/weather-mcp-server",
      "env": {}
    },
    "streaming": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "c:/Users/v-haoguoliang/Desktop/新建文件夹/mcp-streaming-server",
      "env": {}
    }
  }
}
```

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

4. **查看日志：**
   - 检查是否有错误信息
   - 确认网络连接正常

### 如果需要添加其他MCP服务器

1. 确保服务器已正确安装
2. 在配置文件中添加服务器配置
3. 重启应用

## 配置文件格式说明

### stdio类型服务器（推荐）
```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "服务器路径",
      "env": {}
    }
  }
}
```

### SSE类型服务器
```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse",
      "url": "http://127.0.0.1:端口/sse"
    }
  }
}
```

**注意：** SSE类型的服务器必须先启动，否则会出现连接错误。

## 总结

✓ 已移除不工作的figma-dev-mode服务器配置
✓ 已配置可用的Weather MCP服务器
✓ 已验证Weather服务器工作正常
✓ 配置文件已更新

**下一步：** 重启Copilot Code Pro应用以应用更改。

---

**修复时间：** 2026-02-24
**修复人员：** Copilot Code Pro
