# MCP 流式服务器 - 安装指南

## 环境要求

- Python 3.8 或更高版本
- pip (Python 包管理器)

## 安装步骤

### Windows 系统

#### 方法 1: 使用启动脚本（推荐）

1. **双击运行** [`start.bat`](start.bat:1)
   - 脚本会自动创建虚拟环境
   - 自动安装所有依赖
   - 启动服务器

#### 方法 2: 手动安装

1. **打开命令提示符或 PowerShell**

2. **进入项目目录**
   ```cmd
   cd mcp-streaming-server
   ```

3. **创建虚拟环境（可选但推荐）**
   ```cmd
   python -m venv venv
   ```

4. **激活虚拟环境**
   ```cmd
   venv\Scripts\activate
   ```

5. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

6. **启动服务器**
   ```cmd
   python server.py
   ```

### Linux/macOS 系统

1. **打开终端**

2. **进入项目目录**
   ```bash
   cd mcp-streaming-server
   ```

3. **创建虚拟环境（可选但推荐）**
   ```bash
   python3 -m venv venv
   ```

4. **激活虚拟环境**
   ```bash
   source venv/bin/activate
   ```

5. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

6. **启动服务器**
   ```bash
   python server.py
   ```

## 验证安装

### 1. 检查服务器是否运行

打开浏览器访问: http://localhost:8000

你应该看到类似以下的响应：
```json
{
  "name": "通用 MCP 流式服务器",
  "version": "1.0.0",
  "status": "running",
  "tools_count": 3
}
```

### 2. 查看 API 文档

访问: http://localhost:8000/docs

你将看到 Swagger UI 交互式 API 文档。

### 3. 运行测试

在新的终端窗口中：

```bash
# 激活虚拟环境（如果使用）
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 运行测试
python test_client.py
```

## 常见问题

### 问题 1: Python 未找到

**错误信息：**
```
Python was not found
```

**解决方案：**
1. 从 [python.org](https://www.python.org/downloads/) 下载并安装 Python
2. 安装时勾选 "Add Python to PATH"
3. 重新打开命令提示符

### 问题 2: pip 未找到

**错误信息：**
```
'pip' is not recognized as an internal or external command
```

**解决方案：**
```bash
python -m ensurepip --upgrade
```

### 问题 3: 端口 8000 已被占用

**错误信息：**
```
Error: Address already in use
```

**解决方案：**
修改 [`server.py`](server.py:563) 的最后几行，更改端口号：
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8001,  # 改为其他端口
    log_level="info"
)
```

### 问题 4: 依赖安装失败

**解决方案：**
1. 升级 pip：
   ```bash
   python -m pip install --upgrade pip
   ```

2. 使用国内镜像（中国用户）：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

## 依赖说明

项目依赖以下 Python 包：

- **mcp** (>=0.9.0): Model Context Protocol 核心库
- **fastapi** (>=0.104.0): 现代化 Web 框架
- **uvicorn[standard]** (>=0.24.0): ASGI 服务器
- **pydantic** (>=2.5.0): 数据验证
- **sse-starlette** (>=1.8.0): Server-Sent Events 支持
- **python-multipart** (>=0.0.6): 表单数据处理

## 配置选项

### 修改服务器端口

编辑 [`server.py`](server.py:563)：
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,  # 修改此处
    log_level="info"
)
```

### 修改日志级别

可选值: `"critical"`, `"error"`, `"warning"`, `"info"`, `"debug"`, `"trace"`

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    log_level="debug"  # 修改此处
)
```

### 仅本地访问

如果只想在本机访问，修改 host：
```python
uvicorn.run(
    app,
    host="127.0.0.1",  # 仅本地
    port=8000,
    log_level="info"
)
```

## 下一步

安装成功后，请查看以下文档：

- [`README.md`](README.md:1) - 项目概述和使用指南
- [`server.py`](server.py:1) - 服务器源代码
- [`test_client.py`](test_client.py:1) - 测试客户端代码

## 获取帮助

如果遇到问题：

1. 检查 Python 版本: `python --version` (需要 3.8+)
2. 检查 pip 版本: `pip --version`
3. 查看错误日志
4. 参考本文档的常见问题部分