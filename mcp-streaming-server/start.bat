@echo off
chcp 65001 >nul
echo ========================================
echo MCP 流式服务器启动脚本
echo ========================================
echo.

REM 检查是否已安装依赖
if not exist "venv\" (
    echo [1/3] 创建虚拟环境...
    py -m venv venv
    if errorlevel 1 (
        echo 错误: 无法创建虚拟环境
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
) else (
    echo [1/3] 虚拟环境已存在
)

echo.
echo [2/3] 安装依赖...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo ✓ 依赖安装成功

echo.
echo [3/3] 启动服务器...
echo.
echo ========================================
echo 服务器信息
echo ========================================
echo API 文档: http://localhost:8000/docs
echo 工具列表: http://localhost:8000/tools
echo 根路径:   http://localhost:8000/
echo ========================================
echo.
echo 按 Ctrl+C 停止服务器
echo.

py server.py

pause