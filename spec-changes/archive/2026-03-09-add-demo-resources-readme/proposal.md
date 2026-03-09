# 提案：为 demo-resources-mcp 添加 README.md

## 为什么

`demo-resources-mcp` 是工作区中 4 个 MCP 服务器项目之一，但它是**唯一没有 README.md 的项目**。其他三个（weather-mcp-server、custom-tools-mcp、mcp-streaming-server）都有完整的 README 文档。

缺少 README 导致：
- 新开发者无法快速了解项目用途
- GitHub 仓库页面显示空白描述
- 无法了解如何安装、配置和使用该服务
- `hello-world.md` 健康徽章中该项目缺少 📖 文档标记

## 变更内容

为 `demo-resources-mcp/` 目录创建一份完整的 `README.md` 文档，涵盖：

1. 项目简介和功能定位
2. 可用工具清单（get_document、list_documents、search_documents）
3. 内置文档资源（welcome、guide、api）
4. 安装配置步骤
5. MCP 客户端配置示例
6. 使用示例
7. 技术架构说明

## 功能 (Capabilities)

### 新增功能

- `demo-resources-readme`: 为 demo-resources-mcp 项目创建 README.md 文档

### 修改功能

无

## 影响

- 新增文件：`demo-resources-mcp/README.md`
- 受益项目：demo-resources-mcp
- 间接影响：`hello-world.md` 中该项目的健康状态将从缺少 📖 变为拥有 📖
