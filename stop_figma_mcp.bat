@echo off
echo Stopping Figma MCP Server...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq figma-developer-mcp*" 2>nul
taskkill /F /IM figma-developer-mcp.exe 2>nul
echo.
echo Figma MCP Server has been stopped.
timeout /t 2 >nul
