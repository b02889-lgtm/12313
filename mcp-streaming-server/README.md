# MCP 流式服务器

一个支持流式响应的通用 MCP (Model Context Protocol) 服务器框架。

## 功能特性

- ✅ 完整的 MCP 服务器实现
- ✅ 支持流式和非流式工具调用
- ✅ 基于 FastAPI 的高性能异步框架
- ✅ SSE (Server-Sent Events) 流式传输
- ✅ 内置示例工具（文本生成、数字序列、进度报告）
- ✅ 完整的测试客户端
- ✅ 易于扩展和自定义
- ✅ 日志记录和监控功能

## 项目结构

```
mcp-streaming-server/
├── server.py           # MCP 服务器主文件
├── test_client.py      # 测试客户端
├── requirements.txt    # Python 依赖
└── README.md          # 项目文档
```

## 安装

### 1. 安装依赖

```bash
cd mcp-streaming-server
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python server.py
```

服务器将在 `http://localhost:31126` 启动。

## 使用方法

### API 端点

#### 1. 根路径
```
GET /
```
返回服务器基本信息。

#### 2. 列出工具
```
GET /tools
```
返回所有可用工具的列表。

#### 3. 调用工具（非流式）
```
POST /tools/call
Content-Type: application/json

{
  "tool_name": "stream_numbers",
  "arguments": {
    "start": 1,
    "end": 5
  },
  "stream": false
}
```

#### 4. 调用工具（流式）
```
POST /tools/stream
Content-Type: application/json

{
  "tool_name": "stream_text",
  "arguments": {
    "text": "Hello World",
    "chunk_size": 5,
    "delay": 0.1
  },
  "stream": true
}
```

### 内置工具

#### 1. stream_text
流式生成文本，按指定大小分块返回。

**参数：**
- `text` (string, 必需): 要生成的文本内容
- `delay` (number, 可选): 每个数据块之间的延迟（秒），默认 0.1
- `chunk_size` (integer, 可选): 每个数据块的大小，默认 5

**示例：**
```python
{
  "tool_name": "stream_text",
  "arguments": {
    "text": "这是一个测试文本",
    "chunk_size": 3,
    "delay": 0.1
  }
}
```

#### 2. stream_numbers
流式生成数字序列，包含数字及其平方。

**参数：**
- `start` (integer, 可选): 起始数字，默认 1
- `end` (integer, 可选): 结束数字，默认 10
- `delay` (number, 可选): 每个数字之间的延迟（秒），默认 0.2

**示例：**
```python
{
  "tool_name": "stream_numbers",
  "arguments": {
    "start": 1,
    "end": 5,
    "delay": 0.15
  }
}
```

#### 3. stream_progress
流式报告任务进度。

**参数：**
- `total_steps` (integer, 可选): 总步骤数，默认 10
- `step_delay` (number, 可选): 每个步骤之间的延迟（秒），默认 0.3

**示例：**
```python
{
  "tool_name": "stream_progress",
  "arguments": {
    "total_steps": 8,
    "step_delay": 0.2
  }
}
```

## 测试

### 自动测试

运行所有测试：

```bash
python test_client.py
```

### 交互式测试

启动交互式测试模式：

```bash
python test_client.py interactive
```

## 自定义工具

### 注册新工具

在 [`server.py`](server.py:1) 中添加新工具：

```python
async def my_custom_tool(
    param1: str,
    param2: int,
    _stream: bool = True
) -> AsyncGenerator[StreamChunk, None]:
    """自定义工具描述"""
    if not _stream:
        # 非流式：返回完整结果
        return {"result": "complete"}
    
    # 流式：逐块返回
    for i in range(param2):
        await asyncio.sleep(0.1)
        yield StreamChunk(
            content={"data": f"{param1}-{i}"},
            chunk_index=i,
            is_final=(i == param2 - 1)
        )

# 注册工具
mcp_server.register_tool(
    name="my_custom_tool",
    description="我的自定义工具",
    input_schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "参数1"},
            "param2": {"type": "integer", "description": "参数2"}
        },
        "required": ["param1", "param2"]
    },
    handler=my_custom_tool
)
```

## API 文档

启动服务器后，访问以下地址查看交互式 API 文档：

- Swagger UI: http://localhost:31126/docs
- ReDoc: http://localhost:31126/redoc
- MCP端点: http://localhost:31126/mcp

## 技术栈

- **FastAPI**: 现代化的 Python Web 框架
- **Uvicorn**: ASGI 服务器
- **Pydantic**: 数据验证和设置管理
- **SSE (Server-Sent Events)**: 流式数据传输

## 流式响应格式

流式响应使用 SSE 格式，每个数据块格式如下：

```
data: {"content": "...", "chunk_index": 0, "is_final": false}

data: {"content": "...", "chunk_index": 1, "is_final": true}

data: [DONE]
```

## 注意事项

1. 确保在调用流式工具时设置 `stream: true`
2. 流式响应使用 SSE 格式，客户端需要正确解析
3. 工具处理器必须支持 `_stream` 参数
4. 流式工具必须返回 `AsyncGenerator[StreamChunk, None]`

## 日志记录和监控

### 日志配置

服务器内置了完整的日志记录功能，支持以下特性：

- **多级日志**: 支持 DEBUG、INFO、WARNING、ERROR、CRITICAL 级别
- **文件日志**: 自动将日志写入文件，支持日志轮转
- **控制台输出**: 实时在控制台显示彩色日志
- **请求追踪**: 记录所有 API 请求和响应时间

**配置示例：**
```python
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
```

### 监控端点

服务器提供以下监控端点：

| 端点 | 描述 |
|------|------|
| `/health` | 健康检查端点，返回服务器状态 |
| `/metrics` | 性能指标端点，返回请求统计信息 |
| `/status` | 详细状态端点，返回系统资源使用情况 |

**健康检查示例：**
```bash
curl http://localhost:31126/health
```

**响应：**
```json
{
  "status": "healthy",
  "uptime": "2h 30m 15s",
  "version": "1.0.0"
}
```

### 性能指标

监控系统收集以下指标：

- **请求计数**: 总请求数、成功/失败请求数
- **响应时间**: 平均响应时间、P95、P99 延迟
- **活跃连接**: 当前活跃的 SSE 连接数
- **内存使用**: 服务器内存占用情况
- **工具调用统计**: 每个工具的调用次数和耗时

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
