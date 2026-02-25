@echo off
echo Starting Figma MCP Server in background mode...
echo Server will run on port 8080
echo Press Ctrl+C to stop the server
echo.

start /B figma-developer-mcp --figma-api-key figd_1x4FZjXvgeBZN9_8Dt0sntpSjrwjK9vBB7Cw1NaZ --port 8080

echo.
echo Figma MCP Server is now running in the background.
echo You can close this window and the server will continue running.
echo To stop the server, run stop_figma_mcp.bat
echo.
timeout /t 3 >nul
