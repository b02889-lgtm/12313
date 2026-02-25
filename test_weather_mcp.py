#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Weather MCP服务器
"""

import asyncio
import json
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 导入weather服务器的工具
sys.path.insert(0, 'weather-mcp-server')
from server import app as weather_app

async def test_weather_server():
    """测试weather服务器"""
    print("=" * 60)
    print("测试 Weather MCP 服务器")
    print("=" * 60)
    
    # 测试1: 列出工具
    print("\n[测试1] 列出可用工具...")
    try:
        tools = await weather_app.list_tools()
        print(f"✓ 成功获取工具列表，共 {len(tools)} 个工具:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"✗ 获取工具列表失败: {e}")
        return False
    
    # 测试2: 调用get_weather工具
    print("\n[测试2] 测试获取北京天气...")
    try:
        result = await weather_app.call_tool(
            "get_weather",
            {"city": "北京", "units": "m", "lang": "zh"}
        )
        print("✓ 成功获取天气信息:")
        print(result[0].text[:200] + "...")
    except Exception as e:
        print(f"✗ 获取天气失败: {e}")
        return False
    
    # 测试3: 调用get_weather_forecast工具
    print("\n[测试3] 测试获取上海天气预报...")
    try:
        result = await weather_app.call_tool(
            "get_weather_forecast",
            {"city": "上海", "days": 2, "units": "m", "lang": "zh"}
        )
        print("✓ 成功获取天气预报:")
        print(result[0].text[:200] + "...")
    except Exception as e:
        print(f"✗ 获取天气预报失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过！Weather MCP 服务器工作正常")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = asyncio.run(test_weather_server())
    sys.exit(0 if success else 1)
