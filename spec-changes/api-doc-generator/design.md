# 设计：API 文档生成器（api-doc-generator）

## 目标目录结构

```
工作区根目录/
├── docs/                           # 文档源文件目录
│   ├── index.md                   # 文档首页
│   ├── getting-started.md         # 快速入门
│   ├── installation.md            # 安装指南
│   │
│   ├── api/                       # API 参考文档（自动生成）
│   │   ├── index.md              # API 概览
│   │   ├── scripts/              # scripts/ 模块文档
│   │   │   ├── file_utils.md
│   │   │   ├── data_processor.md
│   │   │   └── ...
│   │   ├── demos/                # demos/ 模块文档
│   │   │   └── ...
│   │   └── data-analysis/        # data-analysis/ 模块文档
│   │       └── ...
│   │
│   ├── mcp/                       # MCP 服务文档
│   │   ├── overview.md           # MCP 服务概览
│   │   ├── weather-mcp.md        # 天气 MCP 服务
│   │   ├── demo-resources-mcp.md # 演示资源 MCP
│   │   └── custom-tools-mcp.md   # 自定义工具 MCP
│   │
│   ├── guides/                    # 使用指南
│   │   ├── docstring-style.md    # 文档字符串规范
│   │   ├── type-hints.md         # 类型注解指南
│   │   └── contributing.md       # 贡献指南
│   │
│   └── assets/                    # 静态资源
│       ├── images/
│       └── stylesheets/
│           └── extra.css         # 自定义样式
│
├── site/                          # 【生成】构建后的静态站点
│   └── ...                        # HTML 文件
│
├── mkdocs.yml                     # MkDocs 主配置文件
├── requirements-docs.txt          # 文档工具依赖
│
└── scripts/
    └── gen_ref_pages.py          # API 文档生成脚本
```

## 设计决策

### 1. 文档架构设计

```
┌─────────────────────────────────────────────────────────┐
│                     文档站点首页                          │
│              项目简介、快速链接、特性概览                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ 快速入门   │  │ API 参考   │  │ MCP 文档   │          │
│  │           │  │           │  │           │          │
│  │ 安装配置   │  │ 自动生成   │  │ 手动+自动   │          │
│  │ 基本使用   │  │ 模块文档   │  │ 接口说明   │          │
│  └───────────┘  └───────────┘  └───────────┘          │
│                                                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ 使用指南   │  │ 示例代码   │  │ 更新日志   │          │
│  │           │  │           │  │           │          │
│  │ 最佳实践   │  │ 实战案例   │  │ 版本历史   │          │
│  │ 规范说明   │  │ 常见问题   │  │           │          │
│  └───────────┘  └───────────┘  └───────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. MkDocs 配置设计

#### mkdocs.yml 主配置

```yaml
# mkdocs.yml - MkDocs 主配置文件

site_name: 工作区项目文档
site_description: 自动化工具和 MCP 服务的 API 参考文档
site_author: 项目团队
site_url: https://your-username.github.io/your-repo/

# 仓库信息
repo_name: your-username/your-repo
repo_url: https://github.com/your-username/your-repo
edit_uri: edit/main/docs/

# 主题配置
theme:
  name: material
  language: zh
  
  # 颜色方案
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: 切换到暗色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: 切换到亮色模式
  
  # 功能特性
  features:
    - navigation.instant      # 即时加载
    - navigation.tracking     # 地址栏跟踪
    - navigation.tabs         # 顶部导航标签
    - navigation.sections     # 侧边栏分组
    - navigation.expand       # 侧边栏展开
    - navigation.top          # 返回顶部按钮
    - search.suggest          # 搜索建议
    - search.highlight        # 搜索高亮
    - content.code.copy       # 代码复制按钮
    - content.code.annotate   # 代码注释
  
  # 图标
  icon:
    repo: fontawesome/brands/github
    logo: material/book-open-variant

# 插件
plugins:
  - search:
      lang: 
        - zh
        - en
      separator: '[\s\-\.]+'
  
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          paths: [.]  # 搜索路径
          options:
            show_source: true           # 显示源码链接
            show_root_heading: true     # 显示模块标题
            show_root_full_path: false  # 不显示完整路径
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            docstring_style: google     # Google 风格 docstring
            docstring_section_style: table  # 参数表格形式
            members_order: source       # 按源码顺序
            show_signature_annotations: true  # 显示类型注解
            separate_signature: true    # 分离签名
            merge_init_into_class: true # 合并 __init__ 到类
  
  - gen-files:
      scripts:
        - scripts/gen_ref_pages.py  # 自动生成 API 页面
  
  - literate-nav:
      nav_file: SUMMARY.md
  
  - section-index

# Markdown 扩展
markdown_extensions:
  - admonition              # 提示块
  - pymdownx.details        # 可折叠块
  - pymdownx.superfences:   # 代码块增强
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:     # 代码高亮
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite   # 行内代码高亮
  - pymdownx.tabbed:        # 标签页
      alternate_style: true
  - pymdownx.tasklist:      # 任务列表
      custom_checkbox: true
  - tables                  # 表格
  - attr_list               # 属性列表
  - md_in_html              # HTML 中的 Markdown
  - toc:                    # 目录
      permalink: true
      toc_depth: 3

# 导航结构
nav:
  - 首页: index.md
  - 快速入门:
    - 安装: installation.md
    - 入门: getting-started.md
  - API 参考:
    - api/index.md
    - Scripts 模块: api/scripts/
    - Demos 模块: api/demos/
    - 数据分析: api/data-analysis/
  - MCP 服务:
    - 概览: mcp/overview.md
    - 天气服务: mcp/weather-mcp.md
    - 演示资源: mcp/demo-resources-mcp.md
    - 自定义工具: mcp/custom-tools-mcp.md
  - 使用指南:
    - Docstring 规范: guides/docstring-style.md
    - 类型注解: guides/type-hints.md
    - 贡献指南: guides/contributing.md

# 额外配置
extra:
  # 社交链接
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/your-username

  # 版本信息
  version:
    provider: mike
    default: latest

# 自定义 CSS
extra_css:
  - assets/stylesheets/extra.css
```

### 3. API 文档自动生成脚本

```python
# scripts/gen_ref_pages.py
"""
自动生成 API 参考文档页面

此脚本会扫描指定的源代码目录，为每个 Python 模块生成对应的 Markdown 文档页面。
这些页面使用 mkdocstrings 的 ::: 语法引用模块，实现文档自动生成。
"""

from pathlib import Path
import mkdocs_gen_files

# 需要生成文档的源代码目录
SOURCE_DIRS = [
    ("scripts", "api/scripts"),
    ("demos", "api/demos"),
    ("data-analysis", "api/data-analysis"),
]

# 需要排除的文件模式
EXCLUDE_PATTERNS = [
    "__pycache__",
    "__init__.py",
    "test_*.py",
    "*_test.py",
]

# 导航结构
nav = mkdocs_gen_files.Nav()


def should_exclude(path: Path) -> bool:
    """检查文件是否应该被排除"""
    for pattern in EXCLUDE_PATTERNS:
        if path.match(pattern):
            return True
    return False


def get_module_path(file_path: Path, src_dir: str) -> str:
    """将文件路径转换为模块路径"""
    # 移除 .py 后缀
    parts = list(file_path.with_suffix("").parts)
    # 移除源目录前缀
    if parts[0] == src_dir:
        parts = parts[1:]
    return ".".join([src_dir] + parts)


def generate_doc_page(src_dir: str, doc_dir: str):
    """为指定目录生成文档页面"""
    src_path = Path(src_dir)
    
    if not src_path.exists():
        print(f"警告: 源目录不存在 - {src_dir}")
        return
    
    for py_file in sorted(src_path.rglob("*.py")):
        if should_exclude(py_file):
            continue
        
        # 计算相对路径
        relative_path = py_file.relative_to(src_path)
        
        # 生成文档路径
        doc_path = Path(doc_dir) / relative_path.with_suffix(".md")
        
        # 获取模块路径
        module_path = get_module_path(py_file, src_dir)
        
        # 生成文档内容
        content = f"""# {py_file.stem}

::: {module_path}
    options:
      show_source: true
      show_root_heading: false
      heading_level: 2
"""
        
        # 写入文件
        with mkdocs_gen_files.open(doc_path, "w") as f:
            f.write(content)
        
        # 添加到导航
        nav_parts = [doc_dir] + list(relative_path.with_suffix("").parts)
        nav[nav_parts] = str(doc_path)
        
        # 设置编辑路径（指向源文件）
        mkdocs_gen_files.set_edit_path(doc_path, py_file)


# 生成所有目录的文档
for src_dir, doc_dir in SOURCE_DIRS:
    generate_doc_page(src_dir, doc_dir)

# 生成导航文件
with mkdocs_gen_files.open("api/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
```

### 4. Docstring 规范设计

采用 **Google 风格** docstring，统一所有模块的文档格式：

```python
def example_function(param1: str, param2: int, param3: list = None) -> dict:
    """函数简短描述（一行）。

    函数详细描述。可以包含多行文字，解释函数的用途、
    背景信息、注意事项等。

    Args:
        param1: 第一个参数的描述。如果描述很长，
            可以换行并缩进。
        param2: 第二个参数的描述。
        param3: 第三个参数的描述。默认为 None，
            表示使用空列表。

    Returns:
        返回值的描述。如果返回字典，可以说明键值：
        - key1: 键1的含义
        - key2: 键2的含义

    Raises:
        ValueError: 当 param1 为空字符串时抛出。
        TypeError: 当 param2 不是整数时抛出。

    Examples:
        基本用法示例：

        >>> result = example_function("hello", 42)
        >>> print(result)
        {'status': 'ok', 'value': 42}

        带可选参数的示例：

        >>> result = example_function("test", 10, [1, 2, 3])
        >>> print(result['items'])
        [1, 2, 3]

    Note:
        这里可以添加特别说明或注意事项。

    See Also:
        related_function: 相关函数的引用。
    """
    # 函数实现
    pass


class ExampleClass:
    """类的简短描述。

    类的详细描述，说明类的用途、设计思路等。

    Attributes:
        attr1: 公开属性1的描述。
        attr2: 公开属性2的描述。

    Examples:
        创建和使用实例：

        >>> obj = ExampleClass("value")
        >>> obj.method()
        'result'
    """

    def __init__(self, attr1: str):
        """初始化 ExampleClass 实例。

        Args:
            attr1: 初始化属性1的值。
        """
        self.attr1 = attr1
        self.attr2 = None

    def method(self) -> str:
        """方法的描述。

        Returns:
            方法返回值的描述。
        """
        return "result"
```

### 5. 类型注解规范

```python
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    TypeVar,
    Generic,
)
from pathlib import Path
from dataclasses import dataclass

# 类型别名
FilePath = Union[str, Path]
JsonData = Dict[str, Any]
CallbackFunc = Callable[[str, int], bool]

# 泛型类型
T = TypeVar('T')


def process_file(
    filepath: FilePath,
    encoding: str = "utf-8",
    *,
    callback: Optional[CallbackFunc] = None,
) -> JsonData:
    """处理文件并返回 JSON 数据。

    Args:
        filepath: 文件路径，支持字符串或 Path 对象。
        encoding: 文件编码，默认 UTF-8。
        callback: 可选的回调函数，接收文件名和行数。

    Returns:
        解析后的 JSON 数据。
    """
    pass


def batch_process(
    items: List[T],
    processor: Callable[[T], T],
) -> List[T]:
    """批量处理项目列表。

    Args:
        items: 要处理的项目列表。
        processor: 处理函数。

    Returns:
        处理后的项目列表。
    """
    return [processor(item) for item in items]


@dataclass
class Config:
    """配置数据类。

    Attributes:
        name: 配置名称。
        value: 配置值。
        enabled: 是否启用。
    """
    name: str
    value: Any
    enabled: bool = True
```

### 6. MCP 服务文档模板

```markdown
# Weather MCP 服务

## 概述

天气查询 MCP 服务，提供实时天气数据查询功能。

## 服务信息

| 属性 | 值 |
|------|-----|
| 服务名称 | weather-mcp-server |
| 版本 | 1.0.0 |
| 协议 | MCP (Model Context Protocol) |
| 传输方式 | stdio |

## 可用工具

### get_weather

获取指定城市的天气信息。

**参数**

| 名称 | 类型 | 必填 | 描述 |
|------|------|------|------|
| city | string | 是 | 城市名称（中文或英文） |
| unit | string | 否 | 温度单位，`celsius`（默认）或 `fahrenheit` |

**返回值**

```json
{
    "city": "Beijing",
    "temperature": 25,
    "unit": "celsius",
    "condition": "晴",
    "humidity": 45,
    "wind": "东北风 3级"
}
```

**示例**

请求：
```json
{
    "tool": "get_weather",
    "arguments": {
        "city": "北京"
    }
}
```

响应：
```json
{
    "result": {
        "city": "北京",
        "temperature": 25,
        "condition": "晴"
    }
}
```

**错误码**

| 代码 | 描述 |
|------|------|
| CITY_NOT_FOUND | 无法找到指定的城市 |
| API_ERROR | 天气 API 调用失败 |

## 配置

### 启动命令

```bash
cd weather-mcp-server
python server.py
```

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| WEATHER_API_KEY | 天气 API 密钥 | - |
| WEATHER_API_URL | API 基础 URL | https://api.weather.com |

## 集成示例

### Claude Desktop 配置

```json
{
    "mcpServers": {
        "weather": {
            "command": "python",
            "args": ["server.py"],
            "cwd": "path/to/weather-mcp-server"
        }
    }
}
```
```

### 7. CI/CD 集成配置

```yaml
# .github/workflows/docs.yml
name: 文档构建与部署

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - 'scripts/*.py'
      - 'demos/*.py'
      - 'data-analysis/*.py'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: 安装依赖
        run: |
          pip install -r requirements-docs.txt
      
      - name: 构建文档
        run: |
          mkdocs build --strict
      
      - name: 上传构建产物
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - name: 部署到 GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 8. 文档依赖配置

```txt
# requirements-docs.txt
# MkDocs 核心
mkdocs>=1.5.0
mkdocs-material>=9.4.0

# 自动生成 API 文档
mkdocstrings>=0.24.0
mkdocstrings-python>=1.7.0

# 插件
mkdocs-gen-files>=0.5.0
mkdocs-literate-nav>=0.6.0
mkdocs-section-index>=0.3.0

# Markdown 扩展
pymdown-extensions>=10.0

# 可选：PDF 导出
# mkdocs-pdf-export-plugin>=0.5.10
```

### 9. 文档站点目录结构预览

```
site/                              # 构建后的静态站点
├── index.html                     # 首页
├── installation/
│   └── index.html
├── getting-started/
│   └── index.html
├── api/
│   ├── index.html                # API 概览
│   ├── scripts/
│   │   ├── file_utils/
│   │   │   └── index.html        # file_utils 模块文档
│   │   └── data_processor/
│   │       └── index.html
│   └── ...
├── mcp/
│   ├── overview/
│   │   └── index.html
│   ├── weather-mcp/
│   │   └── index.html
│   └── ...
├── guides/
│   └── ...
├── assets/
│   ├── stylesheets/
│   ├── javascripts/
│   └── images/
├── search/
│   └── search_index.json          # 搜索索引
└── sitemap.xml                    # 站点地图
```

### 10. 版本管理策略

使用 `mike` 工具管理多版本文档：

```bash
# 安装 mike
pip install mike

# 发布新版本
mike deploy --push --update-aliases 1.0.0 latest

# 设置默认版本
mike set-default --push latest

# 查看所有版本
mike list
```

版本策略：
- `latest`: 始终指向最新稳定版
- `x.y.z`: 具体版本号
- `dev`: 开发版（可选）

---

**设计状态**：待审核
**创建日期**：2026-03-04
**作者**：Copilot Code Pro
