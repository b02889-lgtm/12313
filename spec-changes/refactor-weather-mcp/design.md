# 设计：重构 Weather MCP Server (refactor-weather-mcp)

## 1. 目标架构

### 1.1 当前结构 vs 重构后结构

```
【当前】                         【重构后】
weather-mcp-server/             weather-mcp-server/
├── server.py (286行,全部逻辑)   ├── server.py          # MCP 入口 + 路由 (~50行)
├── requirements.txt             ├── config.py           # 配置管理 (~30行)
├── weather-mcp-config.json      ├── services/
├── README.md                    │   ├── __init__.py
└── PROJECT_ANALYSIS.md          │   ├── weather_api.py  # API 客户端 (~60行)
                                 │   └── cache.py        # 内存缓存 (~40行)
                                 ├── tools/
                                 │   ├── __init__.py
                                 │   ├── current.py      # 当前天气工具 (~50行)
                                 │   └── forecast.py     # 天气预报工具 (~60行)
                                 ├── formatters/
                                 │   ├── __init__.py
                                 │   └── weather.py      # 格式化输出 (~40行)
                                 ├── tests/
                                 │   ├── __init__.py
                                 │   ├── test_weather_api.py
                                 │   ├── test_current.py
                                 │   ├── test_forecast.py
                                 │   └── test_cache.py
                                 ├── requirements.txt
                                 ├── weather-mcp-config.json
                                 ├── README.md
                                 └── PROJECT_ANALYSIS.md
```

### 1.2 模块职责划分

```
┌──────────────────────────────────────────┐
│            server.py (入口)               │
│  - MCP Server 实例创建                    │
│  - list_tools() 工具注册                  │
│  - call_tool() 路由分发                   │
└──────┬───────────────┬───────────────────┘
       │               │
  ┌────▼────┐    ┌─────▼─────┐
  │ tools/  │    │ tools/    │
  │current  │    │ forecast  │
  │.py      │    │ .py       │
  └────┬────┘    └─────┬─────┘
       │               │
       └───────┬───────┘
               │
    ┌──────────▼──────────┐
    │  services/          │
    │  weather_api.py     │
    │  (共享 httpx 客户端) │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │  services/cache.py  │
    │  (TTL 内存缓存)      │
    └─────────────────────┘
```

## 2. 详细设计

### 2.1 配置管理 (`config.py`)

将所有硬编码常量提取为配置类，支持环境变量覆盖：

```python
import os

class Config:
    # API 配置
    WEATHER_API_BASE = os.getenv("WEATHER_API_BASE", "https://wttr.in")
    REQUEST_TIMEOUT = float(os.getenv("WEATHER_TIMEOUT", "10.0"))
    
    # 缓存配置
    CACHE_ENABLED = os.getenv("WEATHER_CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL", "600"))  # 默认 10 分钟
    CACHE_MAX_SIZE = int(os.getenv("WEATHER_CACHE_MAX_SIZE", "100"))
    
    # 默认参数
    DEFAULT_UNITS = "m"
    DEFAULT_LANG = "zh"
    VALID_UNITS = {"m", "u"}
    VALID_LANGS = {"zh", "en", "ja", "fr", "de"}
```

### 2.2 Weather API 客户端 (`services/weather_api.py`)

封装 wttr.in API 的调用逻辑，修复 URL 拼接问题，复用 httpx 客户端：

```python
from urllib.parse import quote

class WeatherAPIClient:
    def __init__(self, config: Config):
        self._client: httpx.AsyncClient | None = None
        self._config = config
    
    async def get_client(self) -> httpx.AsyncClient:
        """懒加载并复用 httpx 客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self._config.REQUEST_TIMEOUT)
        return self._client
    
    async def fetch_weather(self, city: str, units: str, lang: str) -> dict:
        """获取天气原始数据（修复 URL 编码问题）"""
        encoded_city = quote(city, safe='')
        url = f"{self._config.WEATHER_API_BASE}/{encoded_city}"
        params = {"format": "j1", "lang": lang}
        # wttr.in 用裸参数表示单位，需特殊处理
        if units == "u":
            params["u"] = ""
        
        client = await self.get_client()
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """关闭客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
```

### 2.3 内存缓存 (`services/cache.py`)

基于 TTL 的简单内存缓存，避免对同一城市的重复请求：

```python
import time
from typing import Any

class TTLCache:
    def __init__(self, ttl: int = 600, max_size: int = 100):
        self._cache: dict[str, tuple[float, Any]] = {}
        self._ttl = ttl
        self._max_size = max_size
    
    def get(self, key: str) -> Any | None:
        """获取缓存值，过期返回 None"""
        if key in self._cache:
            timestamp, value = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存值，超出最大容量时清理最旧的条目"""
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
        self._cache[key] = (time.time(), value)
    
    def _evict_oldest(self):
        """驱逐最旧的缓存条目"""
        if self._cache:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][0])
            del self._cache[oldest_key]
```

缓存 Key 格式：`"{city}:{units}:{lang}"`

### 2.4 工具模块 (`tools/current.py`, `tools/forecast.py`)

每个工具模块负责：
1. 参数验证（二次校验 units/lang 是否在允许范围内）
2. 调用 `WeatherAPIClient`（先查缓存，未命中才请求）
3. 调用 `formatters` 格式化输出

关键改进 - **forecast.py 中的索引安全访问**：
```python
# 旧代码（危险）
morning = hourly[4]
afternoon = hourly[10]
evening = hourly[16]

# 新代码（安全）
def safe_get_hourly(hourly: list, index: int, default: dict = None) -> dict:
    """安全获取 hourly 数组元素"""
    if default is None:
        default = {}
    return hourly[index] if index < len(hourly) else default

morning = safe_get_hourly(hourly, 4)
afternoon = safe_get_hourly(hourly, 10)
evening = safe_get_hourly(hourly, 16)
```

### 2.5 格式化器 (`formatters/weather.py`)

将字符串拼接逻辑从业务函数中分离，便于后续支持不同输出格式（纯文本/Markdown/JSON）：

```python
def format_current_weather(city: str, data: dict, units: str) -> str:
    """格式化当前天气报告"""
    ...

def format_forecast(city: str, weather_data: list, days: int, units: str) -> str:
    """格式化天气预报报告"""
    ...
```

### 2.6 入口改造 (`server.py`)

重构后的 `server.py` 将只保留 MCP 协议相关的注册和路由逻辑（约 50 行），所有业务逻辑委托给子模块：

```python
from tools.current import handle_get_weather
from tools.forecast import handle_get_forecast

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    handlers = {
        "get_weather": handle_get_weather,
        "get_weather_forecast": handle_get_forecast,
    }
    handler = handlers.get(name)
    if handler:
        return await handler(arguments)
    return [TextContent(type="text", text=f"未知工具: {name}")]
```

## 3. 错误处理策略

| 错误类型 | 处理方式 | 用户看到的信息 |
|---------|---------|-------------|
| 参数无效 | 在工具层校验并直接返回 | "错误：城市名称不能为空" |
| HTTP 请求失败 | 在 API 客户端层捕获 | "获取天气失败：无法连接服务" |
| JSON 解析失败 | 在 API 客户端层捕获 | "获取天气失败：数据格式异常" |
| 数据字段缺失 | 使用 `.get()` + 默认值 | 显示 "N/A" |
| 未知异常 | 在路由层兜底 | "内部错误，请稍后重试"（不暴露堆栈） |

## 4. 测试策略

- 使用 `pytest` + `pytest-asyncio` 作为测试框架
- 使用 `respx` 或 `unittest.mock` 来 mock httpx 请求
- 测试覆盖：
  - `test_weather_api.py`：API 客户端的 URL 构造、错误处理
  - `test_current.py`：当前天气数据解析和格式化
  - `test_forecast.py`：预报数据解析、索引安全访问
  - `test_cache.py`：TTL 过期、最大容量驱逐

## 5. 兼容性保证

重构遵循**行为不变原则**：
- MCP 工具名称不变（`get_weather`, `get_weather_forecast`）
- 输入参数 schema 不变
- 输出格式不变（相同的 emoji 布局和文本结构）
- 配置文件 `weather-mcp-config.json` 不变