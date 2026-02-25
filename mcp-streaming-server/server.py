# -*- coding: utf-8 -*-
"""
MCP 流式服务器
支持流式响应的通用 MCP 服务器框架
"""

import asyncio
import json
import os
import time
from typing import AsyncGenerator, Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn


# ==================== 配置管理 ====================

class ServerConfig:
    """服务器配置类"""
    HOST = os.getenv("MCP_HOST", "0.0.0.0")
    PORT = int(os.getenv("MCP_PORT", "31126"))
    LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "info")
    
    @classmethod
    def get_base_url(cls):
        """获取基础 URL"""
        return f"http://{cls.HOST if cls.HOST != '0.0.0.0' else 'localhost'}:{cls.PORT}"


# ==================== 数据模型 ====================

class ToolDefinition(BaseModel):
    """工具定义"""
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    input_schema: Dict[str, Any] = Field(..., description="输入参数的JSON Schema")


class ToolCallRequest(BaseModel):
    """工具调用请求"""
    tool_name: str = Field(..., description="要调用的工具名称")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="工具参数")
    stream: bool = Field(default=False, description="是否使用流式响应")


class ToolResponse(BaseModel):
    """工具响应"""
    content: Any = Field(..., description="响应内容")
    is_error: bool = Field(default=False, description="是否为错误响应")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="元数据")


class StreamChunk(BaseModel):
    """流式数据块"""
    content: Any = Field(..., description="数据块内容")
    chunk_index: int = Field(..., description="数据块索引")
    is_final: bool = Field(default=False, description="是否为最后一个数据块")


# ==================== MCP 服务器核心 ====================

class MCPStreamingServer:
    """MCP 流式服务器核心类"""
    
    def __init__(self, name: str = "MCP Streaming Server", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, callable] = {}
        self.tool_definitions: Dict[str, ToolDefinition] = {}
        
    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: callable
    ):
        """注册工具"""
        self.tools[name] = handler
        self.tool_definitions[name] = ToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema
        )
        print(f"[MCP] 已注册工具: {name}")
    
    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        stream: bool = False
    ) -> AsyncGenerator[StreamChunk, None]:
        """调用工具（支持流式）"""
        if tool_name not in self.tools:
            raise ValueError(f"工具 '{tool_name}' 未找到")
        
        handler = self.tools[tool_name]
        
        if stream:
            # 流式调用
            async for chunk in handler(**arguments, _stream=True):
                yield chunk
        else:
            # 非流式调用
            async for chunk in handler(**arguments, _stream=False):
                yield chunk
    
    def list_tools(self) -> List[ToolDefinition]:
        """列出所有可用工具"""
        return list(self.tool_definitions.values())


# ==================== FastAPI 应用 ====================

# 创建全局服务器实例
mcp_server = MCPStreamingServer(
    name="通用 MCP 流式服务器",
    version="1.0.0"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print(f"[MCP] 服务器启动: {mcp_server.name} v{mcp_server.version}")
    yield
    print("[MCP] 服务器关闭")


app = FastAPI(
    title="MCP Streaming Server",
    description="支持流式响应的通用 MCP 服务器",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": mcp_server.name,
        "version": mcp_server.version,
        "status": "running",
        "tools_count": len(mcp_server.tools)
    }


@app.get("/tools")
async def list_tools():
    """列出所有可用工具"""
    tools = mcp_server.list_tools()
    return {
        "tools": [tool.dict() for tool in tools],
        "count": len(tools)
    }


@app.get("/mcp")
async def mcp_info():
    """MCP协议信息端点"""
    return {
        "name": mcp_server.name,
        "version": mcp_server.version,
        "protocol": "mcp",
        "type": "http",
        "status": "running",
        "tools_count": len(mcp_server.tools),
        "endpoints": {
            "tools": "/tools",
            "call": "/tools/call",
            "stream": "/tools/stream",
            "health": "/health"
        }
    }


@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """调用工具（非流式）"""
    try:
        chunks = []
        async for chunk in mcp_server.call_tool(
            request.tool_name,
            request.arguments,
            stream=False
        ):
            chunks.append(chunk)
        
        return ToolResponse(
            content=chunks[0].content,
            is_error=False,
            metadata={"chunks_count": len(chunks)}
        )
    except Exception as e:
        return ToolResponse(
            content=str(e),
            is_error=True,
            metadata={"error_type": type(e).__name__}
        )


@app.post("/tools/stream")
async def stream_tool(request: ToolCallRequest):
    """调用工具（流式）"""
    request.stream = True
    
    async def generate():
        try:
            async for chunk in mcp_server.call_tool(
                request.tool_name,
                request.arguments,
                stream=True
            ):
                # 将数据块转换为 SSE 格式
                data = json.dumps(chunk.dict(), ensure_ascii=False)
                yield f"data: {data}\n\n"
            
            # 发送完成信号
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_data = json.dumps({
                "content": str(e),
                "is_error": True,
                "error_type": type(e).__name__
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# ==================== 示例工具 ====================

async def stream_text_generator(
    text: str,
    delay: float = 0.1,
    chunk_size: int = 5,
    _stream: bool = True
) -> AsyncGenerator[StreamChunk, None]:
    """流式文本生成器工具"""
    if not _stream:
        # 非流式：返回完整文本
        yield StreamChunk(
            content=text,
            chunk_index=0,
            is_final=True
        )
        return
    
    # 流式：逐块返回
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    
    for idx, chunk in enumerate(chunks):
        await asyncio.sleep(delay)
        yield StreamChunk(
            content=chunk,
            chunk_index=idx,
            is_final=(idx == len(chunks) - 1)
        )


async def stream_numbers(
    start: int = 1,
    end: int = 10,
    delay: float = 0.2,
    _stream: bool = True
) -> AsyncGenerator[StreamChunk, None]:
    """流式数字生成器工具"""
    if not _stream:
        # 非流式：返回数字列表
        yield StreamChunk(
            content=list(range(start, end + 1)),
            chunk_index=0,
            is_final=True
        )
        return
    
    # 流式：逐个返回数字
    for idx, num in enumerate(range(start, end + 1)):
        await asyncio.sleep(delay)
        yield StreamChunk(
            content={"number": num, "square": num ** 2},
            chunk_index=idx,
            is_final=(num == end)
        )


async def stream_progress(
    total_steps: int = 10,
    step_delay: float = 0.3,
    _stream: bool = True
) -> AsyncGenerator[StreamChunk, None]:
    """流式进度报告工具"""
    if not _stream:
        # 非流式：返回最终进度
        yield StreamChunk(
            content={"step": total_steps, "total": total_steps, "progress": 100},
            chunk_index=0,
            is_final=True
        )
        return
    
    # 流式：逐步报告进度
    for step in range(1, total_steps + 1):
        await asyncio.sleep(step_delay)
        progress = (step / total_steps) * 100
        yield StreamChunk(
            content={
                "step": step,
                "total": total_steps,
                "progress": round(progress, 2),
                "status": "进行中" if step < total_steps else "完成"
            },
            chunk_index=step - 1,
            is_final=(step == total_steps)
        )


# ==================== 注册工具 ====================

# 注册流式文本生成器
mcp_server.register_tool(
    name="stream_text",
    description="流式生成文本，按指定大小分块返回",
    input_schema={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "要生成的文本内容"
            },
            "delay": {
                "type": "number",
                "description": "每个数据块之间的延迟（秒）",
                "default": 0.1
            },
            "chunk_size": {
                "type": "integer",
                "description": "每个数据块的大小",
                "default": 5
            }
        },
        "required": ["text"]
    },
    handler=stream_text_generator
)

# 注册流式数字生成器
mcp_server.register_tool(
    name="stream_numbers",
    description="流式生成数字序列，包含数字及其平方",
    input_schema={
        "type": "object",
        "properties": {
            "start": {
                "type": "integer",
                "description": "起始数字",
                "default": 1
            },
            "end": {
                "type": "integer",
                "description": "结束数字",
                "default": 10
            },
            "delay": {
                "type": "number",
                "description": "每个数字之间的延迟（秒）",
                "default": 0.2
            }
        },
        "required": []
    },
    handler=stream_numbers
)

# 注册流式进度报告
mcp_server.register_tool(
    name="stream_progress",
    description="流式报告任务进度",
    input_schema={
        "type": "object",
        "properties": {
            "total_steps": {
                "type": "integer",
                "description": "总步骤数",
                "default": 10
            },
            "step_delay": {
                "type": "number",
                "description": "每个步骤之间的延迟（秒）",
                "default": 0.3
            }
        },
        "required": []
    },
    handler=stream_progress
)


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MCP 流式服务器启动中...".center(60))
    print("=" * 60 + "\n")
    
    print(f"服务器名称: {mcp_server.name}")
    print(f"服务器版本: {mcp_server.version}")
    print(f"已注册工具数: {len(mcp_server.tools)}")
    print("\n可用工具:")
    for tool_name in mcp_server.tools.keys():
        print(f"  - {tool_name}")
    
    base_url = ServerConfig.get_base_url()
    
    print("\n" + "=" * 60)
    print("服务器信息".center(60))
    print("=" * 60)
    print(f"API 文档: {base_url}/docs")
    print(f"工具列表: {base_url}/tools")
    print(f"根路径:   {base_url}/")
    print(f"MCP端点:  {base_url}/mcp")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        app,
        host=ServerConfig.HOST,
        port=ServerConfig.PORT,
        log_level=ServerConfig.LOG_LEVEL
    )