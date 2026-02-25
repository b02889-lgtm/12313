#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证MCP配置
"""

import json
import os
import sys

def verify_mcp_config():
    """验证MCP配置文件"""
    print("=" * 60)
    print("MCP 配置验证")
    print("=" * 60)

    # 配置文件路径
    config_path = r"C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json"

    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        print(f"✗ 配置文件不存在: {config_path}")
        return False

    print(f"✓ 配置文件存在: {config_path}")

    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ 配置文件格式正确（JSON有效）")
    except json.JSONDecodeError as e:
        print(f"✗ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 读取配置文件失败: {e}")
        return False

    # 检查mcpServers
    if "mcpServers" not in config:
        print("✗ 配置文件中缺少 'mcpServers' 字段")
        return False

    print("✓ 配置文件包含 'mcpServers' 字段")

    mcp_servers = config["mcpServers"]
    print(f"\n已配置的MCP服务器数量: {len(mcp_servers)}")

    # 检查每个服务器配置
    for server_name, server_config in mcp_servers.items():
        print(f"\n服务器名称: {server_name}")
        print(f"  类型: {server_config.get('type', 'stdio')}")

        if "command" in server_config:
            print(f"  命令: {server_config['command']}")
            print(f"  参数: {server_config.get('args', [])}")
            print(f"  工作目录: {server_config.get('cwd', 'N/A')}")

            # 检查工作目录是否存在
            cwd = server_config.get('cwd')
            if cwd and os.path.exists(cwd):
                print(f"  ✓ 工作目录存在")
            else:
                print(f"  ⚠ 警告: 工作目录不存在: {cwd}")

        elif "url" in server_config:
            print(f"  URL: {server_config['url']}")
            print(f"  ⚠ 注意: SSE类型服务器需要手动启动")

    # 检查是否有不工作的服务器
    has_sse_servers = any("url" in config for config in mcp_servers.values())
    if has_sse_servers:
        print("\n⚠ 警告: 配置中有SSE类型服务器")
        print("  确保这些服务器已启动，否则会出现连接错误")

    print("\n" + "=" * 60)
    print("✓ MCP配置验证完成")
    print("=" * 60)
    print("\n下一步:")
    print("1. 重启Copilot Code Pro应用")
    print("2. 检查MCP工具是否可用")
    print("3. 如果有问题，查看详细日志")

    return True

if __name__ == "__main__":
    success = verify_mcp_config()
    sys.exit(0 if success else 1)
