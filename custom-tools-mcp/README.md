# 自定义工具 MCP 服务器

这是一个实验性的自定义工具调用能力演示，展示如何通过编写 Python 代码实现自定义 MCP 工具。

## 提供的工具

| 工具名 | 功能说明 |
|--------|----------|
| `text_transform` | 文本转换（大小写、反转、去空格等）|
| `hash_generator` | 生成文本哈希（MD5、SHA1、SHA256 等）|
| `base64_codec` | Base64 编码与解码 |
| `word_counter` | 统计文本信息（字数、字符数等）|
| `json_formatter` | JSON 格式化或压缩 |
| `regex_matcher` | 正则表达式匹配与替换 |
| `timestamp_converter` | Unix 时间戳与日期时间互转 |
| `calculator` | 数学表达式计算器 |

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

## 工具使用示例

### 文本转换
```
工具: text_transform
输入: { "text": "hello world", "operation": "uppercase" }
输出: HELLO WORLD
```

### 哈希生成
```
工具: hash_generator
输入: { "text": "hello", "algorithm": "sha256" }
输出: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### Base64 编码
```
工具: base64_codec
输入: { "text": "你好，世界！", "operation": "encode" }
输出: 5L2g5aW977yM5LiW55WM77yB
```

### JSON 格式化
```
工具: json_formatter
输入: { "json_text": "{\"name\":\"test\"}", "operation": "format" }
输出: 格式化后的 JSON 内容
```

### 时间戳转换
```
工具: timestamp_converter
输入: { "operation": "current" }
输出: 当前时间和 Unix 时间戳
```

### 数学计算
```
工具: calculator
输入: { "expression": "2 + 3 * 4" }
输出: 14
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

## 技术架构

本项目使用以下技术：

- **Python** - 服务器端语言
- **MCP SDK** - Model Context Protocol SDK，提供 MCP 协议支持
- **asyncio** - Python 异步编程框架
- **标准库** - hashlib、base64、re、json、datetime 等

## 自定义工具开发流程

```
用户请求
    │
    ▼
MCP 客户端（Claude）
    │ 发送工具调用请求
    ▼
MCP 服务器（server.py）
    │ call_tool() 分发
    ▼
具体工具处理函数
    │ 执行业务逻辑
    ▼
返回 TextContent 结果
    │
    ▼
MCP 客户端展示结果
```
