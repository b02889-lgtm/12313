#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Figma MCP配置
"""

import json
import os

# 配置文件路径
config_path = r"C:\Users\v-haoguoliang\AppData\Roaming\Code\User\globalStorage\geelib-copilot-code.copilotcodepro\settings\mcp_settings.json"

# 新的配置内容 - 使用stdio模式自动启动
new_config = {
    "mcpServers": {
        "figma-dev-mode": {
            "command": "figma-developer-mcp",
            "args": [
                "--figma-api-key", "YOUR_FIGMA_API_KEY_HERE"
            ],
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
    print("\n重要提示:")
    print("1. 请将 YOUR_FIGMA_API_KEY_HERE 替换为您的真实Figma API Key")
    print("2. 获取API Key: https://www.figma.com/developers/api")
    print("3. 重启Copilot Code Pro应用以应用更改")
except Exception as e:
    print(f"更新配置文件失败: {e}")
