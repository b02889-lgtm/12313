# -*- coding: utf-8 -*-
"""
MCP 流式服务器测试客户端
用于测试服务器的流式响应功能
"""

import asyncio
import aiohttp
import json
import sys
from typing import AsyncGenerator


class MCPStreamClient:
    """MCP 流式客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    async def list_tools(self):
        """列出所有可用工具"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/tools") as response:
                return await response.json()
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """调用工具（非流式）"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/call",
                json={
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "stream": False
                }
            ) as response:
                return await response.json()
    
    async def stream_tool(self, tool_name: str, arguments: dict) -> AsyncGenerator:
        """调用工具（流式）"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/stream",
                json={
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "stream": True
                }
            ) as response:
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        data = line[6:]  # 去掉 'data: ' 前缀
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            continue


async def test_list_tools():
    """测试列出工具"""
    print("\n" + "=" * 60)
    print("测试 1: 列出所有可用工具".center(60))
    print("=" * 60 + "\n")
    
    client = MCPStreamClient()
    try:
        result = await client.list_tools()
        print(f"✓ 成功获取工具列表")
        print(f"  工具数量: {result['count']}")
        print("\n可用工具:")
        for tool in result['tools']:
            print(f"  - {tool['name']}: {tool['description']}")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False


async def test_non_streaming():
    """测试非流式调用"""
    print("\n" + "=" * 60)
    print("测试 2: 非流式调用 (stream_numbers)".center(60))
    print("=" * 60 + "\n")
    
    client = MCPStreamClient()
    try:
        result = await client.call_tool(
            "stream_numbers",
            {"start": 1, "end": 5}
        )
        print(f"✓ 成功调用工具")
        print(f"  响应内容: {result['content']}")
        print(f"  是否错误: {result['is_error']}")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False


async def test_stream_text():
    """测试流式文本生成"""
    print("\n" + "=" * 60)
    print("测试 3: 流式文本生成 (stream_text)".center(60))
    print("=" * 60 + "\n")
    
    client = MCPStreamClient()
    try:
        text = "这是一个测试流式响应的示例文本，每次返回一小块内容。"
        print(f"原始文本: {text}")
        print("\n流式响应:")
        print("-" * 60)
        
        chunks_received = 0
        async for chunk in client.stream_tool(
            "stream_text",
            {"text": text, "chunk_size": 10, "delay": 0.1}
        ):
            chunks_received += 1
            print(f"[块 {chunk['chunk_index'] + 1}] {chunk['content']}", end='', flush=True)
            if chunk['is_final']:
                print(f"\n✓ 完成（共 {chunks_received} 个数据块）")
        
        return True
    except Exception as e:
        print(f"\n✗ 失败: {e}")
        return False


async def test_stream_numbers():
    """测试流式数字生成"""
    print("\n" + "=" * 60)
    print("测试 4: 流式数字生成 (stream_numbers)".center(60))
    print("=" * 60 + "\n")
    
    client = MCPStreamClient()
    try:
        print("生成数字 1-10 及其平方:")
        print("-" * 60)
        
        chunks_received = 0
        async for chunk in client.stream_tool(
            "stream_numbers",
            {"start": 1, "end": 10, "delay": 0.15}
        ):
            chunks_received += 1
            content = chunk['content']
            print(f"[{chunks_received:2d}] 数字: {content['number']:2d}, 平方: {content['square']:3d}")
            if chunk['is_final']:
                print(f"\n✓ 完成（共 {chunks_received} 个数据块）")
        
        return True
    except Exception as e:
        print(f"\n✗ 失败: {e}")
        return False


async def test_stream_progress():
    """测试流式进度报告"""
    print("\n" + "=" * 60)
    print("测试 5: 流式进度报告 (stream_progress)".center(60))
    print("=" * 60 + "\n")
    
    client = MCPStreamClient()
    try:
        print("任务进度报告:")
        print("-" * 60)
        
        chunks_received = 0
        async for chunk in client.stream_tool(
            "stream_progress",
            {"total_steps": 8, "step_delay": 0.2}
        ):
            chunks_received += 1
            content = chunk['content']
            progress_bar = "█" * int(content['progress'] / 10) + "░" * (10 - int(content['progress'] / 10))
            print(f"[步骤 {content['step']}/{content['total']}] {progress_bar} {content['progress']}% - {content['status']}")
            
            if chunk['is_final']:
                print(f"\n✓ 完成（共 {chunks_received} 个数据块）")
        
        return True
    except Exception as e:
        print(f"\n✗ 失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MCP 流式服务器测试套件".center(60))
    print("=" * 60)
    
    tests = [
        ("列出工具", test_list_tools),
        ("非流式调用", test_non_streaming),
        ("流式文本生成", test_stream_text),
        ("流式数字生成", test_stream_numbers),
        ("流式进度报告", test_stream_progress)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ 测试 '{name}' 发生异常: {e}")
            results.append((name, False))
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结".center(60))
    print("=" * 60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    print("\n" + "-" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60 + "\n")
    
    return passed == total


async def interactive_test():
    """交互式测试模式"""
    client = MCPStreamClient()
    
    print("\n" + "=" * 60)
    print("MCP 流式服务器 - 交互式测试".center(60))
    print("=" * 60 + "\n")
    
    # 获取工具列表
    tools_data = await client.list_tools()
    tools = {tool['name']: tool for tool in tools_data['tools']}
    
    print("可用工具:")
    for idx, tool_name in enumerate(tools.keys(), 1):
        print(f"{idx}. {tool_name} - {tools[tool_name]['description']}")
    
    print("\n输入工具编号进行测试 (输入 'q' 退出):")
    
    while True:
        try:
            choice = input("\n> ").strip()
            if choice.lower() == 'q':
                break
            
            idx = int(choice) - 1
            tool_names = list(tools.keys())
            
            if 0 <= idx < len(tool_names):
                tool_name = tool_names[idx]
                print(f"\n正在测试 '{tool_name}'...")
                print("-" * 60)
                
                # 使用默认参数进行流式调用
                async for chunk in client.stream_tool(tool_name, {}):
                    print(f"[块 {chunk['chunk_index']}] {chunk['content']}")
                    if chunk['is_final']:
                        print("✓ 完成")
            else:
                print("无效的选择")
        except ValueError:
            print("请输入有效的数字")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MCP 流式服务器测试客户端".center(60))
    print("=" * 60)
    print("\n请确保服务器正在运行: python server.py")
    print("服务器地址: http://localhost:8000\n")
    
    # 检查命令行参数
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    
    if mode == "interactive":
        print("启动交互式测试模式...")
        asyncio.run(interactive_test())
    else:
        print("启动自动测试模式...")
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)