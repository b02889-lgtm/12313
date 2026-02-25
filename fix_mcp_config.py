#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复MCP配置文件
"""

import json
import os

# 配置文件路径
config_path = r"C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json"

# 新的配置内容
new_config = {
    "mcpServers": {
        "weather": {
            "command": "python",
            "args": [
                "server.py"
            ],
            "cwd": r"c:\Users\v-haoguoliang\Desktop\新建文件夹\weather-mcp-server",
            "env": {}
        }
    }
}

# 写入配置文件
try:
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)
    print(f"配置文件已更新: {config_path}")
    print("\n配置内容:")
    print(json.dumps(new_config, indent=2, ensure_ascii=False))
    print("\n请重启Copilot Code Pro应用以应用更改。")
except Exception as e:
    print(f"更新配置文件失败: {e}")
