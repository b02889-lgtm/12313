#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试Weather MCP服务器
"""

import asyncio
import httpx

async def test_weather_api():
    """测试天气API"""
    print("=" * 60)
    print("测试 Weather API")
    print("=" * 60)
    
    # 测试1: 获取北京天气
    print("\n[测试1] 获取北京天气...")
    try:
        url = "https://wttr.in/北京?format=j1&m&lang=zh"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_condition", [{}])[0]
            temp = current.get("temp_C", "N/A")
            weather_desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
            
            print(f"温度: {temp}°C")
            print(f"天气: {weather_desc}")
            print("✓ 成功获取天气信息")
    except Exception as e:
        print(f"✗ 获取天气失败: {e}")
        return False
    
    # 测试2: 获取上海天气预报
    print("\n[测试2] 获取上海天气预报...")
    try:
        url = "https://wttr.in/上海?format=j1&m&lang=zh"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            weather_data = data.get("weather", [])
            if weather_data:
                day_data = weather_data[0]
                date = day_data.get("date", "未知")
                max_temp = day_data.get("maxtempC", "N/A")
                min_temp = day_data.get("mintempC", "N/A")
                
                print(f"日期: {date}")
                print(f"温度: {min_temp}°C ~ {max_temp}°C")
                print("✓ 成功获取天气预报")
    except Exception as e:
        print(f"✗ 获取天气预报失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ Weather API 测试通过")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = asyncio.run(test_weather_api())
    exit(0 if success else 1)
