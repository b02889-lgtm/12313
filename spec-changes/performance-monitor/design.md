# 设计：性能监控系统（performance-monitor）

## 目标目录结构

```
工作区根目录/
├── perf_monitor/                   # 【新建】性能监控核心模块
│   ├── __init__.py                # 模块入口，导出公共 API
│   ├── core/                      # 核心功能
│   │   ├── __init__.py
│   │   ├── timer.py              # 计时器实现
│   │   ├── profiler.py           # 代码剖析器
│   │   ├── resource_monitor.py   # 资源监控
│   │   └── tracker.py            # 追踪器基类
│   │
│   ├── collectors/                # 数据采集器
│   │   ├── __init__.py
│   │   ├── cpu_collector.py      # CPU 数据采集
│   │   ├── memory_collector.py   # 内存数据采集
│   │   ├── io_collector.py       # I/O 数据采集
│   │   └── mcp_collector.py      # MCP 服务数据采集
│   │
│   ├── storage/                   # 数据存储
│   │   ├── __init__.py
│   │   ├── base.py               # 存储基类
│   │   ├── sqlite_store.py       # SQLite 存储
│   │   ├── json_store.py         # JSON 文件存储
│   │   └── schema.py             # 数据模型定义
│   │
│   ├── analysis/                  # 数据分析
│   │   ├── __init__.py
│   │   ├── statistics.py         # 统计计算
│   │   ├── trend.py              # 趋势分析
│   │   ├── anomaly.py            # 异常检测
│   │   └── comparison.py         # 基准对比
│   │
│   ├── reporting/                 # 报告生成
│   │   ├── __init__.py
│   │   ├── html_report.py        # HTML 报告
│   │   ├── json_export.py        # JSON 导出
│   │   ├── flamegraph.py         # 火焰图生成
│   │   └── templates/            # 报告模板
│   │       └── report.html
│   │
│   ├── alerts/                    # 告警系统
│   │   ├── __init__.py
│   │   ├── rules.py              # 告警规则
│   │   ├── notifier.py           # 通知发送
│   │   └── channels/             # 通知渠道
│   │       ├── __init__.py
│   │       ├── log_channel.py
│   │       ├── email_channel.py
│   │       └── webhook_channel.py
│   │
│   ├── integrations/              # 集成接口
│   │   ├── __init__.py
│   │   ├── decorators.py         # 装饰器
│   │   ├── context_managers.py   # 上下文管理器
│   │   ├── middleware.py         # MCP 中间件
│   │   └── pytest_plugin.py      # pytest 插件
│   │
│   └── cli.py                     # 命令行工具
│
├── perf_data/                     # 【新建】性能数据存储
│   ├── metrics.db                # SQLite 数据库
│   ├── benchmarks/               # 基准测试数据
│   │   └── baseline.json
│   └── profiles/                 # 剖析数据
│       └── .gitkeep
│
├── perf_reports/                  # 【新建】性能报告输出
│   ├── .gitkeep
│   ├── latest/                   # 最新报告
│   └── archive/                  # 历史报告
│
├── benchmarks/                    # 【新建】基准测试用例
│   ├── __init__.py
│   ├── conftest.py               # pytest-benchmark 配置
│   ├── test_scripts_benchmark.py # scripts 模块基准
│   ├── test_data_benchmark.py    # 数据处理基准
│   └── test_mcp_benchmark.py     # MCP 服务基准
│
└── perf_config.yaml              # 【新建】性能监控配置
```

## 设计决策

### 1. 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         应用代码                                 │
│                  @track_performance 装饰器                       │
│                  with monitor() 上下文管理器                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Timer      │    │  Profiler    │    │  Resource    │     │
│  │   计时器      │    │  剖析器       │    │  Monitor     │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             │                                  │
│                    ┌────────▼────────┐                        │
│                    │   Collectors    │                        │
│                    │   数据采集器      │                        │
│                    └────────┬────────┘                        │
│                             │                                  │
├─────────────────────────────┼──────────────────────────────────┤
│                             │                                  │
│                    ┌────────▼────────┐                        │
│                    │    Storage      │                        │
│                    │  SQLite / JSON  │                        │
│                    └────────┬────────┘                        │
│                             │                                  │
├──────────────┬──────────────┼──────────────┬──────────────────┤
│              │              │              │                   │
│    ┌─────────▼────┐   ┌────▼─────┐   ┌────▼─────┐            │
│    │  Analysis    │   │ Reporting│   │  Alerts  │            │
│    │  数据分析     │   │ 报告生成  │   │  告警     │            │
│    └──────────────┘   └──────────┘   └──────────┘            │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 2. 核心数据模型

```python
# perf_monitor/storage/schema.py
"""
性能数据模型定义
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class MetricType(Enum):
    """指标类型"""
    TIMING = "timing"           # 时间指标
    CPU = "cpu"                 # CPU 指标
    MEMORY = "memory"           # 内存指标
    IO = "io"                   # I/O 指标
    COUNTER = "counter"         # 计数器
    GAUGE = "gauge"             # 仪表值


@dataclass
class MetricPoint:
    """单个指标数据点"""
    timestamp: datetime
    metric_name: str
    metric_type: MetricType
    value: float
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "metric_name": self.metric_name,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "tags": self.tags,
        }


@dataclass
class ExecutionRecord:
    """执行记录"""
    id: str
    function_name: str
    module_path: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    success: bool
    error_message: Optional[str] = None
    metrics: List[MetricPoint] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    timestamp: datetime
    iterations: int
    min_time: float
    max_time: float
    mean_time: float
    stddev: float
    percentiles: Dict[str, float]  # p50, p90, p95, p99
    memory_peak: Optional[float] = None


@dataclass
class AlertEvent:
    """告警事件"""
    id: str
    timestamp: datetime
    rule_name: str
    severity: str  # info, warning, critical
    message: str
    metric_value: float
    threshold: float
    context: Dict[str, Any] = field(default_factory=dict)
```

### 3. 计时器设计

```python
# perf_monitor/core/timer.py
"""
高精度计时器实现
"""
import time
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class TimingResult:
    """计时结果"""
    name: str
    duration_ns: int      # 纳秒精度
    duration_ms: float    # 毫秒
    duration_s: float     # 秒
    
    @property
    def formatted(self) -> str:
        """格式化输出"""
        if self.duration_s >= 1:
            return f"{self.duration_s:.3f}s"
        elif self.duration_ms >= 1:
            return f"{self.duration_ms:.3f}ms"
        else:
            return f"{self.duration_ns / 1000:.3f}μs"


class Timer:
    """高精度计时器"""
    
    def __init__(self, name: str = "unnamed"):
        self.name = name
        self._start_time: Optional[int] = None
        self._end_time: Optional[int] = None
    
    def start(self) -> 'Timer':
        """开始计时"""
        self._start_time = time.perf_counter_ns()
        return self
    
    def stop(self) -> TimingResult:
        """停止计时并返回结果"""
        self._end_time = time.perf_counter_ns()
        duration_ns = self._end_time - self._start_time
        return TimingResult(
            name=self.name,
            duration_ns=duration_ns,
            duration_ms=duration_ns / 1_000_000,
            duration_s=duration_ns / 1_000_000_000,
        )
    
    @contextmanager
    def measure(self):
        """上下文管理器方式计时"""
        self.start()
        try:
            yield self
        finally:
            result = self.stop()
            self._last_result = result
    
    @property
    def elapsed(self) -> TimingResult:
        """获取已流逝时间（不停止计时）"""
        current = time.perf_counter_ns()
        duration_ns = current - self._start_time
        return TimingResult(
            name=self.name,
            duration_ns=duration_ns,
            duration_ms=duration_ns / 1_000_000,
            duration_s=duration_ns / 1_000_000_000,
        )


def timed(name: Optional[str] = None, log: bool = True):
    """计时装饰器"""
    def decorator(func: Callable) -> Callable:
        timer_name = name or func.__qualname__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            timer = Timer(timer_name)
            timer.start()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                timing = timer.stop()
                if log:
                    print(f"[TIMING] {timer_name}: {timing.formatted}")
                # 存储到监控系统
                _store_timing(timing)
        
        return wrapper
    return decorator


def _store_timing(result: TimingResult):
    """存储计时结果到监控系统"""
    # 由 storage 模块实现
    pass
```

### 4. 资源监控器设计

```python
# perf_monitor/core/resource_monitor.py
"""
系统资源监控器
"""
import psutil
import os
from dataclasses import dataclass
from typing import Optional, List
from threading import Thread, Event
from queue import Queue
import time


@dataclass
class ResourceSnapshot:
    """资源快照"""
    timestamp: float
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    io_read_bytes: int
    io_write_bytes: int
    open_files: int
    threads: int


class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self, interval: float = 0.1):
        """
        Args:
            interval: 采样间隔（秒）
        """
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self._running = Event()
        self._thread: Optional[Thread] = None
        self._data: Queue = Queue()
        self._snapshots: List[ResourceSnapshot] = []
    
    def start(self):
        """开始监控"""
        self._running.set()
        self._snapshots = []
        self._thread = Thread(target=self._collect, daemon=True)
        self._thread.start()
    
    def stop(self) -> List[ResourceSnapshot]:
        """停止监控并返回数据"""
        self._running.clear()
        if self._thread:
            self._thread.join(timeout=1.0)
        
        # 收集队列中的数据
        while not self._data.empty():
            self._snapshots.append(self._data.get_nowait())
        
        return self._snapshots
    
    def _collect(self):
        """采集循环"""
        while self._running.is_set():
            try:
                snapshot = self._take_snapshot()
                self._data.put(snapshot)
            except Exception:
                pass
            time.sleep(self.interval)
    
    def _take_snapshot(self) -> ResourceSnapshot:
        """采集一次快照"""
        with self.process.oneshot():
            cpu = self.process.cpu_percent()
            mem = self.process.memory_info()
            io = self.process.io_counters() if hasattr(self.process, 'io_counters') else None
            
            return ResourceSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu,
                memory_mb=mem.rss / 1024 / 1024,
                memory_percent=self.process.memory_percent(),
                io_read_bytes=io.read_bytes if io else 0,
                io_write_bytes=io.write_bytes if io else 0,
                open_files=len(self.process.open_files()),
                threads=self.process.num_threads(),
            )
    
    def get_summary(self) -> dict:
        """获取资源使用摘要"""
        if not self._snapshots:
            return {}
        
        cpu_values = [s.cpu_percent for s in self._snapshots]
        mem_values = [s.memory_mb for s in self._snapshots]
        
        return {
            "cpu": {
                "min": min(cpu_values),
                "max": max(cpu_values),
                "avg": sum(cpu_values) / len(cpu_values),
            },
            "memory_mb": {
                "min": min(mem_values),
                "max": max(mem_values),
                "avg": sum(mem_values) / len(mem_values),
            },
            "samples": len(self._snapshots),
        }
```

### 5. 性能追踪装饰器

```python
# perf_monitor/integrations/decorators.py
"""
性能追踪装饰器
"""
from functools import wraps
from typing import Callable, Optional, Dict, Any
import traceback
from datetime import datetime
import uuid

from ..core.timer import Timer
from ..core.resource_monitor import ResourceMonitor
from ..storage import get_storage


def track_performance(
    name: Optional[str] = None,
    track_resources: bool = True,
    sample_rate: float = 1.0,
    tags: Optional[Dict[str, str]] = None,
):
    """
    性能追踪装饰器
    
    Args:
        name: 自定义名称，默认使用函数全名
        track_resources: 是否追踪资源使用
        sample_rate: 采样率 (0.0-1.0)
        tags: 附加标签
    
    Example:
        @track_performance(tags={"module": "data_processing"})
        def process_data(data):
            ...
    """
    def decorator(func: Callable) -> Callable:
        func_name = name or func.__qualname__
        func_tags = tags or {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 采样判断
            import random
            if random.random() > sample_rate:
                return func(*args, **kwargs)
            
            # 初始化追踪
            record_id = str(uuid.uuid4())[:8]
            timer = Timer(func_name)
            monitor = ResourceMonitor() if track_resources else None
            
            # 开始追踪
            start_time = datetime.now()
            timer.start()
            if monitor:
                monitor.start()
            
            success = True
            error_msg = None
            result = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_msg = f"{type(e).__name__}: {str(e)}"
                raise
            finally:
                # 停止追踪
                timing = timer.stop()
                resources = monitor.stop() if monitor else []
                end_time = datetime.now()
                
                # 构建执行记录
                record = {
                    "id": record_id,
                    "function_name": func_name,
                    "module_path": func.__module__,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "duration_ms": timing.duration_ms,
                    "success": success,
                    "error_message": error_msg,
                    "tags": func_tags,
                }
                
                if resources:
                    resource_summary = ResourceMonitor.get_summary.__func__(
                        type('obj', (object,), {'_snapshots': resources})()
                    )
                    record["resources"] = resource_summary
                
                # 存储记录
                storage = get_storage()
                storage.save_execution(record)
        
        return wrapper
    return decorator


def profile(output_file: Optional[str] = None):
    """
    代码剖析装饰器
    
    Args:
        output_file: 剖析结果输出文件（.prof 格式）
    
    Example:
        @profile(output_file="process_data.prof")
        def process_data(data):
            ...
    """
    import cProfile
    import pstats
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            try:
                return profiler.runcall(func, *args, **kwargs)
            finally:
                if output_file:
                    profiler.dump_stats(output_file)
                else:
                    stats = pstats.Stats(profiler)
                    stats.strip_dirs()
                    stats.sort_stats('cumulative')
                    stats.print_stats(20)
        return wrapper
    return decorator
```

### 6. 基准测试框架

```python
# benchmarks/conftest.py
"""
pytest-benchmark 配置
"""
import pytest
import json
from pathlib import Path
from datetime import datetime


# 基准数据存储路径
BENCHMARK_DIR = Path(__file__).parent.parent / "perf_data" / "benchmarks"
BASELINE_FILE = BENCHMARK_DIR / "baseline.json"


@pytest.fixture(scope="session")
def benchmark_baseline():
    """加载基准数据"""
    if BASELINE_FILE.exists():
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    return {}


def pytest_benchmark_compare_machine_info(config, benchmarksession):
    """配置机器信息比较"""
    return True


def pytest_benchmark_group_stats(config, benchmarks, group_by):
    """配置基准分组统计"""
    return benchmarks


@pytest.hookimpl(hookwrapper=True)
def pytest_benchmark_generate_json(config, benchmarks, include_data, machine_info, commit_info):
    """保存基准数据"""
    yield
    
    # 保存为新的基准线（可选）
    save_as_baseline = config.getoption("--benchmark-save-baseline", default=False)
    if save_as_baseline:
        baseline_data = {
            "timestamp": datetime.now().isoformat(),
            "machine_info": machine_info,
            "benchmarks": {
                b["name"]: {
                    "min": b["stats"]["min"],
                    "max": b["stats"]["max"],
                    "mean": b["stats"]["mean"],
                    "stddev": b["stats"]["stddev"],
                }
                for b in benchmarks
            }
        }
        BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)
        with open(BASELINE_FILE, 'w') as f:
            json.dump(baseline_data, f, indent=2)


def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--benchmark-save-baseline",
        action="store_true",
        default=False,
        help="Save current results as new baseline"
    )
    parser.addoption(
        "--benchmark-fail-threshold",
        type=float,
        default=0.1,
        help="Fail if performance degrades by more than this percentage (default: 0.1 = 10%)"
    )
```

```python
# benchmarks/test_scripts_benchmark.py
"""
scripts/ 模块基准测试
"""
import pytest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFileUtilsBenchmark:
    """file_utils 模块基准测试"""
    
    @pytest.fixture
    def sample_file(self, tmp_path):
        """创建测试文件"""
        file_path = tmp_path / "sample.txt"
        file_path.write_text("x" * 10000)  # 10KB 文件
        return file_path
    
    def test_read_file_performance(self, benchmark, sample_file):
        """文件读取性能基准"""
        def read_file():
            return sample_file.read_text()
        
        result = benchmark(read_file)
        assert result is not None
    
    def test_write_file_performance(self, benchmark, tmp_path):
        """文件写入性能基准"""
        file_path = tmp_path / "output.txt"
        content = "x" * 10000
        
        def write_file():
            file_path.write_text(content)
        
        benchmark(write_file)


class TestDataProcessorBenchmark:
    """数据处理基准测试"""
    
    @pytest.fixture
    def sample_data(self):
        """生成测试数据"""
        return [{"id": i, "value": i * 2} for i in range(1000)]
    
    def test_data_transform_performance(self, benchmark, sample_data):
        """数据转换性能基准"""
        def transform(data):
            return [{"id": item["id"], "double_value": item["value"] * 2} for item in data]
        
        result = benchmark(transform, sample_data)
        assert len(result) == 1000
```

### 7. 告警系统设计

```python
# perf_monitor/alerts/rules.py
"""
告警规则定义
"""
from dataclasses import dataclass
from typing import Callable, Optional, Any
from enum import Enum


class Severity(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Operator(Enum):
    """比较操作符"""
    GT = ">"      # 大于
    GE = ">="     # 大于等于
    LT = "<"      # 小于
    LE = "<="     # 小于等于
    EQ = "=="     # 等于
    NE = "!="     # 不等于


@dataclass
class AlertRule:
    """告警规则"""
    name: str
    metric_name: str
    operator: Operator
    threshold: float
    severity: Severity
    message_template: str
    cooldown_seconds: int = 300  # 冷却时间，避免重复告警
    enabled: bool = True
    
    def evaluate(self, value: float) -> bool:
        """评估规则是否触发"""
        ops = {
            Operator.GT: lambda v, t: v > t,
            Operator.GE: lambda v, t: v >= t,
            Operator.LT: lambda v, t: v < t,
            Operator.LE: lambda v, t: v <= t,
            Operator.EQ: lambda v, t: v == t,
            Operator.NE: lambda v, t: v != t,
        }
        return ops[self.operator](value, self.threshold)
    
    def format_message(self, value: float, **context) -> str:
        """格式化告警消息"""
        return self.message_template.format(
            value=value,
            threshold=self.threshold,
            **context
        )


# 预定义规则
DEFAULT_RULES = [
    AlertRule(
        name="high_execution_time",
        metric_name="execution_time_ms",
        operator=Operator.GT,
        threshold=5000,  # 5秒
        severity=Severity.WARNING,
        message_template="函数执行时间过长: {value:.2f}ms > {threshold}ms",
    ),
    AlertRule(
        name="critical_execution_time",
        metric_name="execution_time_ms",
        operator=Operator.GT,
        threshold=30000,  # 30秒
        severity=Severity.CRITICAL,
        message_template="函数执行时间严重超时: {value:.2f}ms > {threshold}ms",
    ),
    AlertRule(
        name="high_memory_usage",
        metric_name="memory_mb",
        operator=Operator.GT,
        threshold=500,  # 500MB
        severity=Severity.WARNING,
        message_template="内存使用过高: {value:.2f}MB > {threshold}MB",
    ),
    AlertRule(
        name="high_cpu_usage",
        metric_name="cpu_percent",
        operator=Operator.GT,
        threshold=90,
        severity=Severity.WARNING,
        message_template="CPU 使用率过高: {value:.1f}% > {threshold}%",
    ),
    AlertRule(
        name="performance_regression",
        metric_name="regression_percent",
        operator=Operator.GT,
        threshold=10,  # 10% 性能退化
        severity=Severity.WARNING,
        message_template="检测到性能退化: {value:.1f}% > {threshold}%",
    ),
]
```

### 8. 报告生成设计

```python
# perf_monitor/reporting/html_report.py
"""
HTML 性能报告生成
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json

from jinja2 import Template


REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>性能监控报告 - {{ report_date }}</title>
    <style>
        :root {
            --primary-color: #4a90d9;
            --success-color: #28a745;
            --warning-color: #ffc107;
            --danger-color: #dc3545;
            --bg-color: #f8f9fa;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: var(--bg-color);
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, var(--primary-color), #357abd);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 { margin: 0 0 10px 0; }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .card h2 { margin-top: 0; color: #333; border-bottom: 2px solid var(--primary-color); padding-bottom: 10px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric-box {
            background: var(--bg-color);
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }
        .metric-value { font-size: 2em; font-weight: bold; color: var(--primary-color); }
        .metric-label { color: #666; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: var(--bg-color); font-weight: 600; }
        tr:hover { background: #f5f5f5; }
        .status-success { color: var(--success-color); }
        .status-warning { color: var(--warning-color); }
        .status-danger { color: var(--danger-color); }
        .chart-container { height: 300px; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 性能监控报告</h1>
            <p>生成时间: {{ report_date }} | 统计周期: {{ period }}</p>
        </div>
        
        <div class="card">
            <h2>📈 概览统计</h2>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-value">{{ summary.total_executions }}</div>
                    <div class="metric-label">总执行次数</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{{ "%.1f"|format(summary.avg_duration_ms) }}ms</div>
                    <div class="metric-label">平均执行时间</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{{ "%.1f"|format(summary.success_rate) }}%</div>
                    <div class="metric-label">成功率</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{{ summary.alert_count }}</div>
                    <div class="metric-label">告警次数</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>⏱️ 函数执行统计</h2>
            <table>
                <thead>
                    <tr>
                        <th>函数名</th>
                        <th>调用次数</th>
                        <th>平均耗时</th>
                        <th>最大耗时</th>
                        <th>成功率</th>
                    </tr>
                </thead>
                <tbody>
                    {% for func in functions %}
                    <tr>
                        <td>{{ func.name }}</td>
                        <td>{{ func.call_count }}</td>
                        <td>{{ "%.2f"|format(func.avg_ms) }}ms</td>
                        <td>{{ "%.2f"|format(func.max_ms) }}ms</td>
                        <td class="{% if func.success_rate >= 99 %}status-success{% elif func.success_rate >= 95 %}status-warning{% else %}status-danger{% endif %}">
                            {{ "%.1f"|format(func.success_rate) }}%
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>📉 执行时间趋势</h2>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
        </div>
        
        {% if alerts %}
        <div class="card">
            <h2>🚨 最近告警</h2>
            <table>
                <thead>
                    <tr>
                        <th>时间</th>
                        <th>级别</th>
                        <th>规则</th>
                        <th>消息</th>
                    </tr>
                </thead>
                <tbody>
                    {% for alert in alerts %}
                    <tr>
                        <td>{{ alert.timestamp }}</td>
                        <td class="status-{{ 'danger' if alert.severity == 'critical' else 'warning' }}">
                            {{ alert.severity }}
                        </td>
                        <td>{{ alert.rule_name }}</td>
                        <td>{{ alert.message }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
    </div>
    
    <script>
        const ctx = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ trend_labels | tojson }},
                datasets: [{
                    label: '平均执行时间 (ms)',
                    data: {{ trend_data | tojson }},
                    borderColor: '#4a90d9',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    </script>
</body>
</html>
"""


class HTMLReportGenerator:
    """HTML 报告生成器"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(
        self,
        summary: Dict[str, Any],
        functions: List[Dict[str, Any]],
        alerts: List[Dict[str, Any]],
        trend_data: Dict[str, List],
    ) -> Path:
        """生成 HTML 报告"""
        template = Template(REPORT_TEMPLATE)
        
        html_content = template.render(
            report_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            period="最近 24 小时",
            summary=summary,
            functions=functions,
            alerts=alerts[-10:],  # 最近 10 条告警
            trend_labels=trend_data.get("labels", []),
            trend_data=trend_data.get("values", []),
        )
        
        # 保存报告
        report_path = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_path.write_text(html_content, encoding='utf-8')
        
        # 更新 latest 链接
        latest_path = self.output_dir / "latest.html"
        if latest_path.exists():
            latest_path.unlink()
        latest_path.write_text(html_content, encoding='utf-8')
        
        return report_path
```

### 9. CLI 工具设计

```python
# perf_monitor/cli.py
"""
性能监控命令行工具
"""
import click
from pathlib import Path
from datetime import datetime, timedelta


@click.group()
def cli():
    """性能监控命令行工具"""
    pass


@cli.command()
@click.option('--period', default='24h', help='统计周期 (例如: 1h, 24h, 7d)')
@click.option('--format', 'output_format', type=click.Choice(['html', 'json']), default='html')
@click.option('--output', '-o', type=click.Path(), help='输出路径')
def report(period: str, output_format: str, output: str):
    """生成性能报告"""
    click.echo(f"生成 {period} 的 {output_format} 报告...")
    # 实现报告生成逻辑
    click.echo("✅ 报告已生成")


@cli.command()
@click.argument('function_name')
@click.option('--last', default=10, help='显示最近 N 条记录')
def stats(function_name: str, last: int):
    """查看函数执行统计"""
    click.echo(f"函数 {function_name} 的最近 {last} 次执行统计:")
    # 实现统计查询逻辑


@cli.command()
@click.option('--severity', type=click.Choice(['info', 'warning', 'critical']), help='筛选告警级别')
@click.option('--last', default='24h', help='时间范围')
def alerts(severity: str, last: str):
    """查看告警记录"""
    click.echo(f"最近 {last} 的告警记录:")
    # 实现告警查询逻辑


@cli.command()
def baseline():
    """设置当前性能数据为基准线"""
    if click.confirm("确定要将当前数据设为新的基准线吗?"):
        # 实现基准线设置逻辑
        click.echo("✅ 基准线已更新")


@cli.command()
def clean():
    """清理过期的性能数据"""
    click.echo("清理 30 天前的历史数据...")
    # 实现清理逻辑
    click.echo("✅ 清理完成")


if __name__ == '__main__':
    cli()
```

### 10. 配置文件设计

```yaml
# perf_config.yaml
# 性能监控系统配置

# 全局设置
global:
  enabled: true
  sample_rate: 1.0  # 采样率 (0.0-1.0)
  log_level: INFO

# 数据存储
storage:
  backend: sqlite  # sqlite / json / both
  sqlite:
    path: perf_data/metrics.db
    retention_days: 30
  json:
    path: perf_data/metrics/
    rotation: daily

# 资源监控
resource_monitor:
  enabled: true
  interval: 0.1  # 采样间隔（秒）
  metrics:
    - cpu
    - memory
    - io

# 基准测试
benchmark:
  baseline_file: perf_data/benchmarks/baseline.json
  fail_threshold: 0.1  # 性能退化阈值 (10%)
  warmup_iterations: 3
  min_iterations: 5

# 告警配置
alerts:
  enabled: true
  channels:
    - type: log
      level: WARNING
    - type: email
      enabled: false
      smtp_server: smtp.example.com
      recipients:
        - admin@example.com
    - type: webhook
      enabled: false
      url: https://hooks.example.com/perf-alerts

  rules:
    - name: high_execution_time
      metric: execution_time_ms
      operator: ">"
      threshold: 5000
      severity: warning
      cooldown: 300

    - name: high_memory
      metric: memory_mb
      operator: ">"
      threshold: 500
      severity: warning
      cooldown: 600

# 报告设置
reporting:
  output_dir: perf_reports
  auto_generate: true
  schedule: "0 9 * * *"  # 每天 9 点生成
  formats:
    - html
    - json
  retention_days: 90

# MCP 服务监控
mcp_monitor:
  enabled: true
  services:
    - name: weather-mcp
      path: weather-mcp-server
    - name: demo-resources-mcp
      path: demo-resources-mcp
```

---

**设计状态**：待审核
**创建日期**：2026-03-04
**作者**：Copilot Code Pro
