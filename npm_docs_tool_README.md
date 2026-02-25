# NPM 文档获取工具

一个用于获取 npm 包最新文档信息的 Python 工具。

---

## ✨ 功能特性

- 📦 获取 npm 包的完整信息
- 🏷️  查看最新版本号
- 📝 获取 README 文档
- 🔍 搜索 npm 包
- 📊 查看依赖关系
- 📅 获取更新时间

---

## 📦 安装依赖

```bash
pip install requests
```

---

## 🚀 使用方法

### 1. 获取包信息

```bash
python npm_docs_tool.py <package_name>
```

**示例：**
```bash
python npm_docs_tool.py express
```

**输出：**
```
============================================================
📦 包名: express
🏷️  版本: 4.18.2
📝 描述: Fast, unopinionated, minimalist web framework
👤 作者: TJ Holowaychuk
📄 许可证: MIT
🔑 关键词: express, framework, web, http, rest, restful

👥 维护者:
  - dougwilson (doug@somethingdoug.com)
  - hemanth.hm (hemanth.hm@gmail.com)

🔗 链接:
  - NPM: https://www.npmjs.com/package/express
  - 主页: http://expressjs.com/
  - 仓库: git+https://github.com/expressjs/express.git

📅 最后更新: 2023-03-01 12:34:56
============================================================
```

---

### 2. 获取 README 文档

```bash
python npm_docs_tool.py <package_name> readme
```

**示例：**
```bash
python npm_docs_tool.py lodash readme
```

---

### 3. 查看依赖关系

```bash
python npm_docs_tool.py <package_name> deps
```

**示例：**
```bash
python npm_docs_tool.py react deps
```

**输出：**
```
📦 react v18.2.0 的依赖:

生产依赖:
  - loose-envify: ^1.1.0
  - object-assign: ^4.1.1

开发依赖:
  - @types/react: ^18.0.0
  - jest: ^29.0.0

对等依赖:
  - react: ^18.0.0
```

---

### 4. 搜索 npm 包

```bash
python npm_docs_tool.py search <query>
```

**示例：**
```bash
python npm_docs_tool.py search figma
```

**输出：**
```
找到 3106 个结果:

1. figma (v0.0.1)
   
2. @figma/plugin-typings (v1.123.0)
   Typings for the Figma Plugin API

3. @figma/rest-api-spec (v0.36.0)
   Typings for the Figma REST API

4. figma-js (v1.16.1-0)
   A simple wrapper for the Figma API

...
```

---

## 📚 API 使用

### Python 代码中使用

```python
from npm_docs_tool import NPMDocsTool

# 创建工具实例
tool = NPMDocsTool()

# 获取包信息
info = tool.get_package_metadata("express")
print(info)

# 获取最新版本
version = tool.get_latest_version("react")
print(f"最新版本: {version}")

# 搜索包
results = tool.search_packages("http server")
for pkg in results['results']:
    print(f"{pkg['name']}: {pkg['description']}")

# 获取依赖
deps = tool.get_dependencies("vue")
print(deps)
```

---

## 🔧 方法说明

### `get_package_info(package_name)`
获取 npm 包的完整信息（来自 npm registry）

**参数：**
- `package_name` (str): npm 包名

**返回：**
- `dict`: 包含完整包信息的字典

---

### `get_latest_version(package_name)`
获取包的最新版本号

**参数：**
- `package_name` (str): npm 包名

**返回：**
- `str`: 最新版本号

---

### `get_package_readme(package_name)`
获取包的 README 文档

**参数：**
- `package_name` (str): npm 包名

**返回：**
- `str`: README 内容

---

### `get_package_metadata(package_name)`
获取包的元数据摘要

**参数：**
- `package_name` (str): npm 包名

**返回：**
- `dict`: 包含元数据的字典
  - `name`: 包名
  - `version`: 版本
  - `description`: 描述
  - `author`: 作者
  - `license`: 许可证
  - `keywords`: 关键词列表
  - `maintainers`: 维护者列表
  - `links`: 相关链接
  - `time`: 时间信息

---

### `search_packages(query, limit=10)`
搜索 npm 包

**参数：**
- `query` (str): 搜索关键词
- `limit` (int): 返回结果数量，默认 10

**返回：**
- `dict`: 搜索结果
  - `total`: 总结果数
  - `results`: 结果列表

---

### `get_dependencies(package_name, version=None)`
获取包的依赖关系

**参数：**
- `package_name` (str): npm 包名
- `version` (str, optional): 版本号，默认最新版本

**返回：**
- `dict`: 依赖信息
  - `dependencies`: 生产依赖
  - `devDependencies`: 开发依赖
  - `peerDependencies`: 对等依赖
  - `optionalDependencies`: 可选依赖

---

### `format_package_info(package_name)`
格式化输出包信息

**参数：**
- `package_name` (str): npm 包名

**返回：**
- `str`: 格式化的字符串

---

## 🌐 数据源

- **NPM Registry:** https://registry.npmjs.org
- **NPM Website:** https://www.npmjs.com

---

## ⚠️ 注意事项

1. **网络连接** - 需要稳定的网络连接访问 npm registry
2. **速率限制** - npm API 有速率限制，请合理使用
3. **编码问题** - Windows 终端可能显示乱码，建议使用支持 UTF-8 的终端
4. **包不存在** - 如果包不存在，会返回错误信息

---

## 📝 示例场景

### 场景 1: 检查包的最新版本

```bash
python npm_docs_tool.py react
```

### 场景 2: 查看包的依赖

```bash
python npm_docs_tool.py express deps
```

### 场景 3: 搜索相关包

```bash
python npm_docs_tool.py search "http server"
```

### 场景 4: 获取包的 README

```bash
python npm_docs_tool.py lodash readme
```

---

## 🎯 使用技巧

1. **批量查询** - 可以在脚本中循环查询多个包
2. **版本比较** - 使用 `get_latest_version()` 检查是否有更新
3. **依赖分析** - 使用 `get_dependencies()` 分析项目依赖
4. **包发现** - 使用 `search_packages()` 发现相关包

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**创建时间：** 2026-02-05
**Python 版本：** 3.13+
**依赖：** requests
