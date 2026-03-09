# 自定义工具 MCP 服务器

一个沙箱化的 Python 代码片段执行器，通过 MCP 协议暴露为可调用工具。支持在对话中直接运行 Python 代码，适合快速验证算法、数据转换、生成测试数据等场景。

## 提供的工具

| 工具名 | 功能说明 | 必需参数 | 可选参数 |
|--------|----------|----------|----------|
| `run_python_snippet` | 在沙箱中执行 Python 代码片段，返回 stdout 和返回值 | `code` (string) | `timeout` (integer, 默认 10 秒) |

## 🔒 安全机制

所有代码在执行前会经过 AST 静态扫描，以下内容会被拦截：

**禁止的内建函数：**
`open`、`exec`、`compile`、`eval`、`breakpoint`、`input`

**禁止导入的模块：**
`os`、`subprocess`、`shutil`、`socket`、`urllib`、`requests`、`httpx`、`ftplib`、`smtplib`、`imaplib`、`poplib`、`ctypes`、`cffi`

**预注入的安全标准库（可直接使用）：**
`math`、`random`、`json`、`re`、`datetime`、`collections`、`itertools`、`functools`、`string`、`hashlib`、`base64`

> ⚠️ 以上列表以 `server.py` 中的 `BLOCKED_NAMES`、`BLOCKED_MODULES` 和 `safe_globals` 为准。

## 安装与运行

### 1. 安装依赖

```bash
cd custom-tools-mcp
pip install -r requirements.txt
```

### 2. 测试运行

```bash
python server.py
```

### 3. 配置到 MCP 设置

在 Claude 的 MCP 配置中添加以下内容：

```json
{
  "mcpServers": {
    "custom-tools": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "c:\\Users\\v-haoguoliang\\Desktop\\新建文件夹\\custom-tools-mcp"
    }
  }
}
```

## 使用示例

### 示例 1：数学计算

```json
{
  "code": "import math\nresult = math.factorial(10)\nprint(f'10! = {result}')"
}
```

输出：
```
10! = 3628800
```

### 示例 2：数据处理

```json
{
  "code": "data = [3, 1, 4, 1, 5, 9, 2, 6]\nsorted_data = sorted(data)\nprint(f'排序后: {sorted_data}')\nprint(f'平均值: {sum(data)/len(data):.2f}')"
}
```

输出：
```
排序后: [1, 1, 2, 3, 4, 5, 6, 9]
平均值: 3.88
```

### 示例 3：JSON 处理

```json
{
  "code": "import json\ndata = {'name': '测试', 'values': [1, 2, 3]}\nprint(json.dumps(data, ensure_ascii=False, indent=2))"
}
```

输出：
```json
{
  "name": "测试",
  "values": [1, 2, 3]
}
```

### 示例 4：带超时的长时间计算

```json
{
  "code": "total = sum(i**2 for i in range(1000000))\nprint(f'前 100 万个平方数之和: {total}')",
  "timeout": 30
}
```

## 技术架构

```
用户请求（code + timeout）
    │
    ▼
┌──────────────────────┐
│  AST 静态安全扫描     │ ← 检查 import 和危险函数调用
│  (禁止模块/函数黑名单) │
└──────────┬───────────┘
           │ 通过
           ▼
┌──────────────────────┐
│  构建沙箱命名空间     │ ← 安全内建 + 11 个标准库
│  (safe_globals)       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  线程池异步执行       │ ← asyncio.wait_for(timeout)
│  (捕获 stdout/stderr) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  格式化输出           │ ← 代码 + stdout + 返回值 / 错误
└──────────────────────┘
```

## 如何添加新工具

在 `server.py` 中按照以下步骤添加新工具：

1. **在 `list_tools()` 函数中注册工具**：
```python
Tool(
    name="my_new_tool",
    description="工具描述",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "参数描述"
            }
        },
        "required": ["param1"]
    }
)
```

2. **在 `call_tool()` 函数中添加分发**：
```python
elif name == "my_new_tool":
    return await handle_my_new_tool(arguments)
```

3. **实现工具处理函数**：
```python
async def handle_my_new_tool(args: dict) -> list[TextContent]:
    param1 = args["param1"]
    # 处理逻辑
    result = f"处理结果: {param1}"
    return [TextContent(type="text", text=result)]
```
