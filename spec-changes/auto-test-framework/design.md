# 设计：自动化测试框架（auto-test-framework）

## 目标目录结构

```
工作区根目录/
├── tests/                           # 【新建】测试根目录
│   ├── __init__.py                 # 包初始化
│   ├── conftest.py                 # pytest 全局配置和 fixtures
│   │
│   ├── unit/                       # 单元测试
│   │   ├── __init__.py
│   │   ├── test_file_utils.py      # file_utils.py 的测试
│   │   ├── test_data_processor.py  # data_processor.py 的测试
│   │   ├── test_calculator.py      # calculator.py 的测试
│   │   └── test_xml_validator.py   # xml_tag_validator.py 的测试
│   │
│   ├── integration/                # 集成测试
│   │   ├── __init__.py
│   │   ├── test_weather_mcp.py     # 天气 MCP 服务测试
│   │   ├── test_demo_resources.py  # demo-resources MCP 测试
│   │   └── test_mcp_integration.py # MCP 服务整体集成测试
│   │
│   └── e2e/                        # 端到端测试
│       ├── __init__.py
│       ├── test_data_analysis_flow.py  # 数据分析完整流程测试
│       └── test_file_processing.py     # 文件处理流程测试
│
├── test-reports/                   # 【新建】测试报告目录
│   ├── .gitkeep                    # 保持目录结构
│   ├── coverage/                   # 覆盖率报告
│   │   └── htmlcov/               # HTML 覆盖率报告
│   └── results/                    # 测试结果报告
│       └── report.html            # HTML 测试报告
│
├── pytest.ini                      # 【新建】pytest 主配置文件
├── pyproject.toml                  # 【更新】添加测试相关配置
├── .coveragerc                     # 【新建】覆盖率配置
├── tox.ini                         # 【新建】多环境测试配置（可选）
│
├── .github/                        # 【新建】GitHub 配置
│   └── workflows/
│       └── tests.yml              # CI 测试工作流
│
└── Makefile                        # 【新建】测试执行快捷命令
```

## 设计决策

### 1. 测试分层策略

```
┌─────────────────────────────────────────────────────────┐
│                     端到端测试 (E2E)                      │
│         验证完整业务流程，模拟真实使用场景                   │
│                    执行时间：较长                         │
├─────────────────────────────────────────────────────────┤
│                     集成测试 (Integration)                │
│         验证模块间交互，测试 MCP 服务通信                   │
│                    执行时间：中等                         │
├─────────────────────────────────────────────────────────┤
│                     单元测试 (Unit)                       │
│         验证单个函数/类的行为，快速反馈                     │
│                    执行时间：很短                         │
└─────────────────────────────────────────────────────────┘
```

| 测试层级 | 占比目标 | 执行频率 | Mock 程度 |
|----------|----------|----------|-----------|
| 单元测试 | 70% | 每次提交 | 完全 Mock 外部依赖 |
| 集成测试 | 20% | 每次 PR | 部分 Mock |
| 端到端测试 | 10% | 每日/发布前 | 无 Mock |

### 2. pytest 配置设计

#### pytest.ini 配置

```ini
[pytest]
# 测试发现
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 输出格式
addopts = 
    -v                          # 详细输出
    --tb=short                  # 简短的 traceback
    --strict-markers            # 严格的标记检查
    -ra                         # 显示所有非通过测试的原因

# 标记注册
markers =
    unit: 单元测试
    integration: 集成测试
    e2e: 端到端测试
    slow: 慢速测试（超过 1 秒）
    mcp: MCP 服务相关测试
    requires_network: 需要网络连接

# 日志配置
log_cli = true
log_cli_level = INFO
log_file = test-reports/test.log
log_file_level = DEBUG

# 超时配置
timeout = 30
timeout_method = thread

# 过滤警告
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

#### conftest.py 全局 Fixtures

```python
"""
tests/conftest.py - 全局测试配置和 Fixtures
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock

# 添加项目根目录到 Python 路径
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / 'scripts'))
sys.path.insert(0, str(ROOT_DIR / 'demos'))


# ============ 通用 Fixtures ============

@pytest.fixture(scope="session")
def project_root():
    """返回项目根目录路径"""
    return ROOT_DIR


@pytest.fixture(scope="session")
def test_data_dir(project_root):
    """返回测试数据目录"""
    return project_root / "tests" / "data"


@pytest.fixture
def temp_dir(tmp_path):
    """提供临时目录，测试后自动清理"""
    return tmp_path


@pytest.fixture
def sample_csv_data():
    """提供示例 CSV 数据"""
    return """name,age,city
Alice,30,Beijing
Bob,25,Shanghai
Charlie,35,Guangzhou"""


@pytest.fixture
def sample_json_data():
    """提供示例 JSON 数据"""
    return {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ],
        "metadata": {"version": "1.0"}
    }


# ============ Mock Fixtures ============

@pytest.fixture
def mock_mcp_server():
    """Mock MCP 服务器连接"""
    mock = MagicMock()
    mock.is_connected.return_value = True
    mock.send_request.return_value = {"status": "ok"}
    return mock


@pytest.fixture
def mock_http_client(mocker):
    """Mock HTTP 请求"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    
    return mocker.patch('requests.get', return_value=mock_response)


# ============ 辅助函数 ============

@pytest.fixture
def assert_file_content():
    """提供文件内容断言辅助函数"""
    def _assert(filepath, expected_content):
        with open(filepath, 'r', encoding='utf-8') as f:
            actual = f.read()
        assert actual == expected_content, f"文件内容不匹配\n预期: {expected_content}\n实际: {actual}"
    return _assert


# ============ Markers 处理 ============

def pytest_configure(config):
    """配置自定义标记"""
    config.addinivalue_line("markers", "unit: 单元测试")
    config.addinivalue_line("markers", "integration: 集成测试")
    config.addinivalue_line("markers", "e2e: 端到端测试")
    config.addinivalue_line("markers", "slow: 慢速测试")
    config.addinivalue_line("markers", "mcp: MCP相关测试")


def pytest_collection_modifyitems(config, items):
    """根据目录自动添加标记"""
    for item in items:
        # 根据路径自动标记
        if "/unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "/e2e/" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
```

### 3. 测试覆盖率配置

#### .coveragerc 配置

```ini
[run]
# 要测量覆盖率的源代码目录
source = 
    scripts
    demos
    data-analysis

# 分支覆盖
branch = True

# 并行测试支持
parallel = True

# 忽略的文件模式
omit = 
    */tests/*
    */__pycache__/*
    */venv/*
    */.venv/*
    */site-packages/*
    setup.py
    conftest.py

[report]
# 排除不需要覆盖的代码
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

# 忽略空文件
ignore_errors = True

# 覆盖率精度
precision = 2

# 显示缺失行号
show_missing = True

# 最低覆盖率要求（低于此值测试失败）
fail_under = 70

[html]
# HTML 报告输出目录
directory = test-reports/coverage/htmlcov

# 报告标题
title = 自动化测试覆盖率报告

[xml]
# XML 报告输出（用于 CI）
output = test-reports/coverage/coverage.xml
```

### 4. 测试报告系统设计

```
┌─────────────────────────────────────────────────────────┐
│                    测试执行                              │
│                      │                                  │
│          ┌──────────┴──────────┐                       │
│          ▼                     ▼                        │
│    pytest-html            pytest-cov                    │
│    (结果报告)              (覆盖率报告)                   │
│          │                     │                        │
│          ▼                     ▼                        │
│   test-reports/          test-reports/                  │
│   results/               coverage/                      │
│   report.html            htmlcov/index.html             │
│          │                     │                        │
│          └──────────┬──────────┘                       │
│                     ▼                                   │
│              历史报告归档                                 │
│        test-reports/archive/                            │
│        YYYY-MM-DD_HHMMSS/                               │
└─────────────────────────────────────────────────────────┘
```

#### 报告归档脚本

```python
# scripts/archive_test_reports.py
"""
测试报告归档工具
每次测试后自动归档报告，便于历史对比
"""
import os
import shutil
from datetime import datetime
from pathlib import Path


def archive_reports():
    """归档当前测试报告"""
    report_dir = Path("test-reports")
    archive_dir = report_dir / "archive"
    
    # 创建时间戳目录
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    target_dir = archive_dir / timestamp
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制报告文件
    for item in ["results", "coverage"]:
        src = report_dir / item
        if src.exists():
            shutil.copytree(src, target_dir / item)
    
    # 清理旧归档（保留最近 10 次）
    archives = sorted(archive_dir.iterdir(), reverse=True)
    for old_archive in archives[10:]:
        shutil.rmtree(old_archive)
    
    print(f"报告已归档到: {target_dir}")


if __name__ == "__main__":
    archive_reports()
```

### 5. 测试执行脚本设计

#### Makefile 快捷命令

```makefile
# Makefile - 测试执行快捷命令

.PHONY: test test-unit test-integration test-e2e test-cov test-report clean-test

# 默认测试命令
test:
	pytest tests/ -v

# 单元测试
test-unit:
	pytest tests/unit/ -v -m unit

# 集成测试
test-integration:
	pytest tests/integration/ -v -m integration

# 端到端测试
test-e2e:
	pytest tests/e2e/ -v -m e2e

# 带覆盖率的测试
test-cov:
	pytest tests/ --cov --cov-report=html --cov-report=xml

# 生成完整测试报告
test-report:
	pytest tests/ \
		--cov \
		--cov-report=html \
		--cov-report=xml \
		--html=test-reports/results/report.html \
		--self-contained-html
	python scripts/archive_test_reports.py

# 快速测试（只运行单元测试，不生成报告）
test-quick:
	pytest tests/unit/ -v -q --tb=line

# 并行测试（加速）
test-parallel:
	pytest tests/ -v -n auto

# 监听模式（文件变化时自动运行测试）
test-watch:
	ptw tests/unit/ -- -v -q

# 清理测试产物
clean-test:
	rm -rf test-reports/results/*
	rm -rf test-reports/coverage/*
	rm -rf .pytest_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
```

### 6. CI/CD 集成配置

#### GitHub Actions 工作流

```yaml
# .github/workflows/tests.yml
name: 自动化测试

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.10"

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov pytest-html pytest-xdist
          pip install -r requirements.txt || true
      
      - name: 运行单元测试
        run: |
          pytest tests/unit/ -v --tb=short
      
      - name: 运行集成测试
        run: |
          pytest tests/integration/ -v --tb=short
      
      - name: 生成覆盖率报告
        run: |
          pytest tests/ \
            --cov \
            --cov-report=xml \
            --cov-report=html \
            --cov-fail-under=70
      
      - name: 上传覆盖率报告
        uses: codecov/codecov-action@v4
        with:
          file: test-reports/coverage/coverage.xml
          fail_ci_if_error: true
      
      - name: 上传测试报告
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports
          path: test-reports/
          retention-days: 30

  lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: 安装 lint 工具
        run: pip install flake8 black isort
      
      - name: 代码风格检查
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
          isort --check-only .
```

### 7. 现有测试文件迁移计划

| 原文件 | 目标位置 | 改造内容 |
|--------|----------|----------|
| `test_demo.py` | `tests/unit/test_demo.py` | 重构为 pytest 风格，修复 import |
| `test_calculator_skill.py` | `tests/unit/test_calculator.py` | 重构为 pytest 风格 |
| `test_skills.py` | `tests/unit/test_skills.py` | 重构为 pytest 风格 |
| `test_weather_api.py` | `tests/integration/test_weather_api.py` | 添加 mock，标记为集成测试 |
| `test_weather_mcp.py` | `tests/integration/test_weather_mcp.py` | 修复 sys.path，添加 mock |

### 8. 测试数据管理

```
tests/
├── data/                          # 测试数据目录
│   ├── fixtures/                  # 固定测试数据
│   │   ├── sample_users.json
│   │   ├── sample_data.csv
│   │   └── config_template.json
│   │
│   ├── mocks/                     # Mock 响应数据
│   │   ├── weather_api_response.json
│   │   └── mcp_server_response.json
│   │
│   └── golden/                    # 期望输出（黄金文件）
│       ├── expected_report.md
│       └── expected_analysis.csv
```

### 9. 测试编写规范

#### 命名规范

```python
# 测试文件：test_<模块名>.py
# 测试类：Test<功能名>
# 测试函数：test_<行为描述>_<预期结果>

# 示例
class TestFileUtils:
    def test_read_file_returns_content_when_file_exists(self):
        ...
    
    def test_read_file_raises_error_when_file_not_found(self):
        ...
    
    def test_write_file_creates_new_file_successfully(self):
        ...
```

#### AAA 模式

```python
def test_calculate_sum_returns_correct_result():
    # Arrange（准备）
    calculator = Calculator()
    a, b = 2, 3
    
    # Act（执行）
    result = calculator.add(a, b)
    
    # Assert（断言）
    assert result == 5
```

#### 参数化测试

```python
@pytest.mark.parametrize("input_a,input_b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_with_various_inputs(input_a, input_b, expected):
    calculator = Calculator()
    assert calculator.add(input_a, input_b) == expected
```

### 10. 性能基准设计

```python
# tests/benchmarks/test_performance.py
"""性能基准测试（可选，与性能监控提案配合）"""

import pytest


@pytest.mark.benchmark(group="file_operations")
def test_file_read_performance(benchmark, temp_file):
    """文件读取性能基准"""
    def read_file():
        with open(temp_file, 'r') as f:
            return f.read()
    
    result = benchmark(read_file)
    assert result is not None


@pytest.mark.benchmark(group="data_processing")
def test_data_processor_performance(benchmark, sample_data):
    """数据处理性能基准"""
    from data_processor import process_data
    
    result = benchmark(process_data, sample_data)
    assert len(result) > 0
```

---

**设计状态**：待审核
**创建日期**：2026-03-04
**作者**：Copilot Code Pro
