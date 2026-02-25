# 天气MCP服务器

一个功能强大的天气查询MCP服务器，可以查询全球城市的当前天气和天气预报。

## 功能特性

- 🌤️ **实时天气查询**：获取全球任意城市的当前天气信息
- 📅 **天气预报**：支持1-3天的天气预报
- 🌍 **多语言支持**：支持中文、英文、日文、法文、德文
- 🌡️ **多单位支持**：支持摄氏度和华氏度
- 🎨 **美观输出**：格式化的天气报告，易于阅读

## 安装步骤

### 1. 安装依赖

确保已安装Python 3.8或更高版本，然后安装所需的依赖包：

```bash
cd weather-mcp-server
pip install -r requirements.txt
```

### 2. 配置MCP服务器

将以下配置添加到您的Claude Desktop配置文件中：

**Windows配置文件位置：**
`%APPDATA%\Claude\claude_desktop_config.json`

**配置内容：**
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

**注意：** 请将 `cwd` 路径修改为您实际的 `weather-mcp-server` 目录路径。

### 3. 重启Claude Desktop

配置完成后，重启Claude Desktop以加载新的MCP服务器。

## 使用方法

### 查询当前天气

在Claude中输入：

```
查询北京的天气
```

或

```
What's the weather in New York?
```

### 查询天气预报

在Claude中输入：

```
查询上海未来3天的天气预报
```

或

```
Get the 2-day weather forecast for Tokyo
```

## 可用工具

### 1. get_weather

获取指定城市的当前天气信息。

**参数：**
- `city` (必需): 城市名称，支持中文或英文
- `units` (可选): 温度单位，`m` 表示摄氏度（默认），`u` 表示华氏度
- `lang` (可选): 语言，`zh`（中文，默认）、`en`（英文）、`ja`（日文）、`fr`（法文）、`de`（德文）

**示例：**
```json
{
  "city": "北京",
  "units": "m",
  "lang": "zh"
}
```

### 2. get_weather_forecast

获取指定城市的天气预报。

**参数：**
- `city` (必需): 城市名称，支持中文或英文
- `days` (可选): 预报天数，1-3天（默认为1）
- `units` (可选): 温度单位，`m` 表示摄氏度（默认），`u` 表示华氏度
- `lang` (可选): 语言，`zh`（中文，默认）、`en`（英文）、`ja`（日文）、`fr`（法文）、`de`（德文）

**示例：**
```json
{
  "city": "上海",
  "days": 3,
  "units": "m",
  "lang": "zh"
}
```

## 天气信息说明

### 当前天气包含：
- 🌡️ 当前温度
- 🤗 体感温度
- ☁️ 天气状况
- 💧 湿度
- 💨 风速和风向
- 📊 气压
- 👁️ 能见度
- ☀️ 紫外线指数

### 天气预报包含：
- 📆 日期
- 🌡️ 温度范围（最高、最低、平均）
- 🌅 早上天气
- ☀️ 下午天气
- 🌙 晚上天气

## 支持的城市

支持全球主要城市，包括但不限于：

**中国：** 北京、上海、广州、深圳、杭州、成都、重庆、武汉、西安、南京等

**国际：** New York、London、Tokyo、Paris、Sydney、Dubai、Singapore等

## 技术细节

- **数据源：** wttr.in API（免费、无需API密钥）
- **协议：** MCP (Model Context Protocol)
- **编程语言：** Python 3.8+
- **主要依赖：** mcp、httpx

## 故障排除

### 问题：无法连接到天气服务

**解决方案：**
1. 检查网络连接
2. 确认防火墙设置
3. 稍后重试

### 问题：MCP服务器未加载

**解决方案：**
1. 检查配置文件路径是否正确
2. 确认Python已正确安装
3. 查看Claude Desktop日志获取详细错误信息
4. 确保所有依赖已正确安装

### 问题：天气信息不准确

**解决方案：**
- wttr.in API使用多种数据源，某些小城市可能数据不够精确
- 尝试使用更大的邻近城市名称

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！

## 更新日志

### v1.0.0 (2024-02-05)
- 初始版本发布
- 支持当前天气查询
- 支持天气预报（1-3天）
- 多语言和多单位支持
