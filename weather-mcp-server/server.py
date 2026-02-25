#!/usr/bin/env python3
"""
天气MCP服务器
提供天气查询功能的MCP服务器
"""

import asyncio
import json
import logging
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建MCP服务器实例
app = Server("weather-server")

# 天气API配置
WEATHER_API_BASE = "https://wttr.in"

@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="get_weather",
            description="获取指定城市的当前天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称（支持中文或英文，如：北京、Shanghai、New York）"
                    },
                    "units": {
                        "type": "string",
                        "description": "温度单位：m（公制，摄氏度）或 u（美制，华氏度）",
                        "enum": ["m", "u"],
                        "default": "m"
                    },
                    "lang": {
                        "type": "string",
                        "description": "语言：zh（中文）、en（英文）等",
                        "enum": ["zh", "en", "ja", "fr", "de"],
                        "default": "zh"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_weather_forecast",
            description="获取指定城市的天气预报",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称（支持中文或英文，如：北京、Shanghai、New York）"
                    },
                    "days": {
                        "type": "integer",
                        "description": "预报天数（1-3天）",
                        "minimum": 1,
                        "maximum": 3,
                        "default": 1
                    },
                    "units": {
                        "type": "string",
                        "description": "温度单位：m（公制，摄氏度）或 u（美制，华氏度）",
                        "enum": ["m", "u"],
                        "default": "m"
                    },
                    "lang": {
                        "type": "string",
                        "description": "语言：zh（中文）、en（英文）等",
                        "enum": ["zh", "en", "ja", "fr", "de"],
                        "default": "zh"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """调用工具"""
    try:
        if name == "get_weather":
            return await get_current_weather(arguments)
        elif name == "get_weather_forecast":
            return await get_weather_forecast(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"未知工具: {name}"
            )]
    except Exception as e:
        logger.error(f"工具调用错误: {e}")
        return [TextContent(
            type="text",
            text=f"错误: {str(e)}"
        )]

async def get_current_weather(args: dict) -> list[TextContent]:
    """获取当前天气"""
    city = args.get("city", "")
    units = args.get("units", "m")
    lang = args.get("lang", "zh")
    
    if not city:
        return [TextContent(
            type="text",
            text="错误：请提供城市名称"
        )]
    
    try:
        # 使用wttr.in API获取天气
        url = f"{WEATHER_API_BASE}/{city}?format=j1&{units}&lang={lang}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        
        # 解析天气数据
        current = data.get("current_condition", [{}])[0]
        
        temp = current.get("temp_C", "N/A") if units == "m" else current.get("temp_F", "N/A")
        feels_like = current.get("FeelsLikeC", "N/A") if units == "m" else current.get("FeelsLikeF", "N/A")
        humidity = current.get("humidity", "N/A")
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
        wind_speed = current.get("windspeedKmph", "N/A")
        wind_dir = current.get("winddir16Point", "N/A")
        pressure = current.get("pressure", "N/A")
        visibility = current.get("visibility", "N/A")
        uv_index = current.get("uvIndex", "N/A")
        
        # 构建天气报告
        unit_symbol = "°C" if units == "m" else "°F"
        
        weather_report = f"""
🌤️ {city} 当前天气
{'='*40}

🌡️ 温度: {temp}{unit_symbol}
🤗 体感温度: {feels_like}{unit_symbol}
☁️ 天气状况: {weather_desc}
💧 湿度: {humidity}%
💨 风速: {wind_speed} km/h
🧭 风向: {wind_dir}
📊 气压: {pressure} hPa
👁️ 能见度: {visibility} km
☀️ 紫外线指数: {uv_index}

📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return [TextContent(
            type="text",
            text=weather_report
        )]
        
    except httpx.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        return [TextContent(
            type="text",
            text=f"获取天气信息失败: 无法连接到天气服务。请检查网络连接或稍后重试。"
        )]
    except Exception as e:
        logger.error(f"获取天气错误: {e}")
        return [TextContent(
            type="text",
            text=f"获取天气信息失败: {str(e)}"
        )]

async def get_weather_forecast(args: dict) -> list[TextContent]:
    """获取天气预报"""
    city = args.get("city", "")
    days = min(max(args.get("days", 1), 1), 3)
    units = args.get("units", "m")
    lang = args.get("lang", "zh")
    
    if not city:
        return [TextContent(
            type="text",
            text="错误：请提供城市名称"
        )]
    
    try:
        # 使用wttr.in API获取天气预报
        url = f"{WEATHER_API_BASE}/{city}?format=j1&{units}&lang={lang}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        
        # 解析预报数据
        weather_data = data.get("weather", [])
        
        if not weather_data:
            return [TextContent(
                type="text",
                text=f"无法获取 {city} 的天气预报"
            )]
        
        # 构建预报报告
        unit_symbol = "°C" if units == "m" else "°F"
        
        forecast_report = f"""
📅 {city} 天气预报（未来{days}天）
{'='*50}
"""
        
        for i in range(min(days, len(weather_data))):
            day_data = weather_data[i]
            date = day_data.get("date", "未知日期")
            max_temp = day_data.get("maxtempC", "N/A") if units == "m" else day_data.get("maxtempF", "N/A")
            min_temp = day_data.get("mintempC", "N/A") if units == "m" else day_data.get("mintempF", "N/A")
            avg_temp = day_data.get("avgtempC", "N/A") if units == "m" else day_data.get("avgtempF", "N/A")
            
            # 获取每小时天气（取几个关键时间点）
            hourly = day_data.get("hourly", [])
            if hourly:
                morning = hourly[4]  # 早上7点
                afternoon = hourly[10]  # 下午1点
                evening = hourly[16]  # 晚上7点
                
                morning_weather = morning.get("weatherDesc", [{}])[0].get("value", "未知")
                afternoon_weather = afternoon.get("weatherDesc", [{}])[0].get("value", "未知")
                evening_weather = evening.get("weatherDesc", [{}])[0].get("value", "未知")
                
                forecast_report += f"""
📆 日期: {date}
🌡️ 温度范围: {min_temp}{unit_symbol} ~ {max_temp}{unit_symbol} (平均: {avg_temp}{unit_symbol})
🌅 早上: {morning_weather}
☀️ 下午: {afternoon_weather}
🌙 晚上: {evening_weather}
{'─'*50}
"""
            else:
                forecast_report += f"""
📆 日期: {date}
🌡️ 温度范围: {min_temp}{unit_symbol} ~ {max_temp}{unit_symbol} (平均: {avg_temp}{unit_symbol})
{'─'*50}
"""
        
        forecast_report += f"\n📅 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return [TextContent(
            type="text",
            text=forecast_report
        )]
        
    except httpx.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        return [TextContent(
            type="text",
            text=f"获取天气预报失败: 无法连接到天气服务。请检查网络连接或稍后重试。"
        )]
    except Exception as e:
        logger.error(f"获取预报错误: {e}")
        return [TextContent(
            type="text",
            text=f"获取天气预报失败: {str(e)}"
        )]

async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
