#!/usr/bin/env python3
"""
自定义工具 MCP 服务器
提供 run_python_snippet 工具 —— 可在对话中像 read_file / execute_command 一样直接调用
用于执行 Python 代码片段并返回结果
"""

import asyncio
import sys
import io
import traceback
import contextlib
import textwrap
import ast
from typing import Any

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("错误: 请先安装 MCP SDK: pip install mcp", file=sys.stderr)
    sys.exit(1)

# 创建服务器
server = Server("custom-tools-server")


# ============================================================
# 工具注册
# ============================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="run_python_snippet",
            description=(
                "执行一段 Python 代码并返回 stdout 输出与执行结果。"
                "适合快速验证算法、进行数据转换、生成测试数据等。"
                "仅允许使用标准库，不允许文件写入或网络请求。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要执行的 Python 代码（支持多行）"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "超时秒数，默认 10 秒",
                        "default": 10
                    }
                },
                "required": ["code"]
            }
        )
    ]


# ============================================================
# 工具调用处理
# ============================================================

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "run_python_snippet":
        return await handle_run_python_snippet(arguments)
    return [TextContent(type="text", text=f"未知工具: {name}")]


# ============================================================
# run_python_snippet 实现
# ============================================================

# 禁止调用的危险模块和函数
BLOCKED_NAMES = {
    "open", "exec", "compile",
    "eval",       # 不允许二次 eval
    "breakpoint", "input",
}
BLOCKED_MODULES = {
    "os", "subprocess", "shutil", "socket",
    "urllib", "requests", "httpx", "ftplib",
    "smtplib", "imaplib", "poplib",
    "ctypes", "cffi",
}


def _is_safe_code(code: str) -> tuple[bool, str]:
    """静态检查代码安全性（AST 扫描）"""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"语法错误: {e}"

    for node in ast.walk(tree):
        # 检查 import
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [alias.name.split(".")[0] for alias in node.names]
                if isinstance(node, ast.Import)
                else ([node.module.split(".")[0]] if node.module else [])
            )
            for mod in names:
                if mod in BLOCKED_MODULES:
                    return False, f"禁止导入模块: {mod}"

        # 检查危险函数调用
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in BLOCKED_NAMES:
                    return False, f"禁止调用函数: {node.func.id}"

    return True, ""


async def handle_run_python_snippet(args: dict) -> list[TextContent]:
    code = args.get("code", "")
    timeout = int(args.get("timeout", 10))

    if not code.strip():
        return [TextContent(type="text", text="错误: 代码不能为空")]

    # 安全检查
    safe, reason = _is_safe_code(code)
    if not safe:
        return [TextContent(type="text", text=f"安全检查未通过: {reason}")]

    # 在线程池中运行（防止阻塞事件循环）
    loop = asyncio.get_event_loop()
    result = await asyncio.wait_for(
        loop.run_in_executor(None, _execute_code, code),
        timeout=timeout
    )

    return [TextContent(type="text", text=result)]


def _execute_code(code: str) -> str:
    """在隔离命名空间中执行代码，捕获 stdout/stderr"""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    # 隔离的全局命名空间（只暴露安全内建）
    safe_globals = {
        "__builtins__": {
            k: v for k, v in __builtins__.__dict__.items()  # type: ignore
            if k not in BLOCKED_NAMES and not k.startswith("__")
        },
        "__name__": "__snippet__",
    }
    # 允许常用标准库
    import math, random, json, re, datetime, collections, itertools, functools, string, hashlib, base64
    safe_globals.update({
        "math": math,
        "random": random,
        "json": json,
        "re": re,
        "datetime": datetime,
        "collections": collections,
        "itertools": itertools,
        "functools": functools,
        "string": string,
        "hashlib": hashlib,
        "base64": base64,
    })

    local_ns: dict = {}

    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(textwrap.dedent(code), safe_globals, local_ns)  # noqa: S102
    except Exception:
        tb = traceback.format_exc()
        output = stdout_buf.getvalue()
        return _format_result(code, output, error=tb)

    output = stdout_buf.getvalue()
    stderr_out = stderr_buf.getvalue()

    # 尝试获取最后一个表达式的值
    last_val = None
    try:
        tree = ast.parse(textwrap.dedent(code))
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_val = eval(  # noqa: S307
                compile(ast.Expression(body=tree.body[-1].value), "<snippet>", "eval"),
                safe_globals,
                local_ns,
            )
    except Exception:
        pass

    return _format_result(code, output, stderr=stderr_out, last_val=last_val)


def _format_result(code: str, output: str, error: str = "", stderr: str = "", last_val=None) -> str:
    lines = []
    lines.append("```python")
    lines.append(code.strip())
    lines.append("```")
    lines.append("")

    if output:
        lines.append("**输出 (stdout):**")
        lines.append("```")
        lines.append(output.rstrip())
        lines.append("```")

    if stderr:
        lines.append("**标准错误 (stderr):**")
        lines.append("```")
        lines.append(stderr.rstrip())
        lines.append("```")

    if error:
        lines.append("**执行错误:**")
        lines.append("```")
        lines.append(error.rstrip())
        lines.append("```")

    if last_val is not None and not output:
        lines.append("**返回值:**")
        lines.append(f"`{repr(last_val)}`")

    if not output and not error and not stderr and last_val is None:
        lines.append("*(代码执行完毕，无输出)*")

    return "\n".join(lines)


# ============================================================
# 启动
# ============================================================

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
