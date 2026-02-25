# MCP 流式服务器 - 使用示例

## 目录

- [Python 客户端示例](#python-客户端示例)
- [JavaScript/Node.js 示例](#javascriptnodejs-示例)
- [cURL 命令示例](#curl-命令示例)
- [实际应用场景](#实际应用场景)

## Python 客户端示例

### 示例 1: 基础非流式调用

```python
import requests

# 调用工具（非流式）
response = requests.post(
    'http://localhost:8000/tools/call',
    json={
        'tool_name': 'stream_numbers',
        'arguments': {
            'start': 1,
            'end': 5,
            'delay': 0.1
        },
        'stream': False
    }
)

result = response.json()
print(f"结果: {result['content']}")
print(f"是否错误: {result['is_error']}")
```

### 示例 2: 流式调用

```python
import requests
import json

# 流式调用工具
response = requests.post(
    'http://localhost:8000/tools/stream',
    json={
        'tool_name': 'stream_text',
        'arguments': {
            'text': '这是一个流式传输的示例文本',
            'chunk_size': 5,
            'delay': 0.1
        },
        'stream': True
    },
    stream=True
)

# 处理流式响应
for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = line[6:]  # 去掉 'data: ' 前缀
            if data == '[DONE]':
                print("\n完成!")
                break
            try:
                chunk = json.loads(data)
                print(chunk['content'], end='', flush=True)
            except json.JSONDecodeError:
                pass
```

### 示例 3: 使用 aiohttp 异步调用

```python
import asyncio
import aiohttp
import json

async def stream_example():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/tools/stream',
            json={
                'tool_name': 'stream_progress',
                'arguments': {
                    'total_steps': 5,
                    'step_delay': 0.3
                }
            }
        ) as response:
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    chunk = json.loads(data)
                    print(f"进度: {chunk['content']['progress']}%")

asyncio.run(stream_example())
```

## JavaScript/Node.js 示例

### 示例 1: 使用 fetch API（浏览器）

```javascript
// 非流式调用
async function callTool() {
    const response = await fetch('http://localhost:8000/tools/call', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tool_name: 'stream_numbers',
            arguments: {
                start: 1,
                end: 5
            },
            stream: false
        })
    });
    
    const result = await response.json();
    console.log('结果:', result.content);
}

callTool();
```

### 示例 2: 流式调用（浏览器）

```javascript
async function streamTool() {
    const response = await fetch('http://localhost:8000/tools/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tool_name: 'stream_text',
            arguments: {
                text: '这是流式传输的文本',
                chunk_size: 5,
                delay: 0.1
            }
        })
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.substring(6);
                if (data === '[DONE]') {
                    console.log('\n完成!');
                    return;
                }
                try {
                    const parsed = JSON.parse(data);
                    process.stdout.write(parsed.content);
                } catch (e) {
                    // 忽略解析错误
                }
            }
        }
    }
}

streamTool();
```

### 示例 3: Node.js 使用 axios

```javascript
const axios = require('axios');

// 流式调用
async function streamWithAxios() {
    const response = await axios({
        method: 'post',
        url: 'http://localhost:8000/tools/stream',
        data: {
            tool_name: 'stream_progress',
            arguments: {
                total_steps: 10,
                step_delay: 0.2
            }
        },
        responseType: 'stream'
    });
    
    response.data.on('data', (chunk) => {
        const lines = chunk.toString().split('\n');
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.substring(6);
                if (data === '[DONE]') {
                    console.log('\n完成!');
                    return;
                }
                try {
                    const parsed = JSON.parse(data);
                    console.log(`进度: ${parsed.content.progress}%`);
                } catch (e) {
                    // 忽略
                }
            }
        }
    });
}

streamWithAxios();
```

## cURL 命令示例

### 示例 1: 列出所有工具

```bash
curl http://localhost:8000/tools
```

### 示例 2: 非流式调用

```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "stream_numbers",
    "arguments": {
      "start": 1,
      "end": 5
    },
    "stream": false
  }'
```

### 示例 3: 流式调用

```bash
curl -X POST http://localhost:8000/tools/stream \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "stream_text",
    "arguments": {
      "text": "Hello, World!",
      "chunk_size": 3,
      "delay": 0.1
    }
  }' \
  --no-buffer
```

### 示例 4: Windows PowerShell

```powershell
# 非流式调用
Invoke-RestMethod -Uri "http://localhost:8000/tools/call" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "tool_name": "stream_numbers",
    "arguments": {"start": 1, "end": 5}
  }'
```

## 实际应用场景

### 场景 1: 实时日志监控

```python
import requests
import json

def monitor_logs():
    """实时监控系统日志"""
    response = requests.post(
        'http://localhost:8000/tools/stream',
        json={
            'tool_name': 'stream_progress',
            'arguments': {
                'total_steps': 100,
                'step_delay': 0.5
            }
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]
                if data == '[DONE]':
                    break
                chunk = json.loads(data)
                # 处理日志数据
                print(f"[{chunk['content']['step']}] 进度: {chunk['content']['progress']}%")

monitor_logs()
```

### 场景 2: 实时数据处理

```python
import requests
import json

def process_stream_data():
    """实时处理数据流"""
    response = requests.post(
        'http://localhost:8000/tools/stream',
        json={
            'tool_name': 'stream_numbers',
            'arguments': {
                'start': 1,
                'end': 100,
                'delay': 0.05
            }
        },
        stream=True
    )
    
    total = 0
    count = 0
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]
                if data == '[DONE]':
                    break
                chunk = json.loads(data)
                number = chunk['content']['number']
                total += number
                count += 1
                
                # 实时计算平均值
                avg = total / count
                print(f"当前平均值: {avg:.2f}")

process_stream_data()
```

### 场景 3: Web 应用集成（React）

```javascript
import React, { useState, useEffect } from 'react';

function StreamingComponent() {
    const [chunks, setChunks] = useState([]);
    const [isStreaming, setIsStreaming] = useState(false);
    
    const startStream = async () => {
        setIsStreaming(true);
        setChunks([]);
        
        const response = await fetch('http://localhost:8000/tools/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tool_name: 'stream_text',
                arguments: {
                    text: '实时流式传输到 React 应用',
                    chunk_size: 5,
                    delay: 0.1
                }
            })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.substring(6);
                    if (data === '[DONE]') {
                        setIsStreaming(false);
                        return;
                    }
                    try {
                        const parsed = JSON.parse(data);
                        setChunks(prev => [...prev, parsed.content]);
                    } catch (e) {}
                }
            }
        }
    };
    
    return (
        <div>
            <button onClick={startStream} disabled={isStreaming}>
                {isStreaming ? '传输中...' : '开始流式传输'}
            </button>
            <div>
                {chunks.map((chunk, i) => (
                    <span key={i}>{chunk}</span>
                ))}
            </div>
        </div>
    );
}

export default StreamingComponent;
```

### 场景 4: 命令行工具

```python
#!/usr/bin/env python3
"""
MCP 流式命令行工具
"""
import sys
import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='MCP 流式客户端')
    parser.add_argument('tool', help='工具名称')
    parser.add_argument('--text', help='文本参数')
    parser.add_argument('--start', type=int, default=1, help='起始数字')
    parser.add_argument('--end', type=int, default=10, help='结束数字')
    parser.add_argument('--steps', type=int, default=10, help='步骤数')
    
    args = parser.parse_args()
    
    # 构建参数
    arguments = {}
    if args.text:
        arguments['text'] = args.text
    if args.tool == 'stream_numbers':
        arguments['start'] = args.start
        arguments['end'] = args.end
    if args.tool == 'stream_progress':
        arguments['total_steps'] = args.steps
    
    # 调用工具
    response = requests.post(
        'http://localhost:8000/tools/stream',
        json={'tool_name': args.tool, 'arguments': arguments},
        stream=True
    )
    
    # 显示结果
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]
                if data == '[DONE]':
                    print('\n完成!')
                    break
                chunk = json.loads(data)
                print(chunk['content'])

if __name__ == '__main__':
    main()
```

使用示例：
```bash
# 流式文本
python cli_tool.py stream_text --text "Hello, World!"

# 流式数字
python cli_tool.py stream_numbers --start 1 --end 20

# 流式进度
python cli_tool.py stream_progress --steps 15
```

## 更多资源

- [README.md](README.md:1) - 项目概述
- [INSTALLATION.md](INSTALLATION.md:1) - 安装指南
- [server.py](server.py:1) - 服务器源代码
- [test_client.py](test_client.py:1) - 完整测试客户端