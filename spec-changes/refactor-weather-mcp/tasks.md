# 任务：重构 Weather MCP Server (refactor-weather-mcp)

## 实现任务清单

### 阶段 1：基础设施搭建
- [ ] **T1.1** 创建目录结构：`services/`、`tools/`、`formatters/`、`tests/` 目录及 `__init__.py`
- [ ] **T1.2** 创建 `config.py`，提取所有硬编码常量（API 地址、超时、默认参数），支持环境变量覆盖
- [ ] **T1.3** 更新 `requirements.txt`，添加测试依赖（`pytest`、`pytest-asyncio`、`respx`）

### 阶段 2：核心服务层重构
- [ ] **T2.1** 实现 `services/weather_api.py` — WeatherAPIClient 类：
  - 修复 URL 编码问题（使用 `urllib.parse.quote`）
  - 修复 units 参数拼接（改为正确的查询参数格式）
  - 实现 httpx 客户端懒加载和复用
  - 实现 `close()` 资源清理方法
- [ ] **T2.2** 实现 `services/cache.py` — TTLCache 类：
  - 基于时间戳的 TTL 过期机制
  - LRU 风格的最大容量驱逐策略
  - 缓存 Key 格式：`"{city}:{units}:{lang}"`

### 阶段 3：工具模块拆分
- [ ] **T3.1** 实现 `tools/current.py` — `handle_get_weather()` 函数：
  - 从原 `get_current_weather()` 迁移逻辑
  - 添加输入参数二次校验（units/lang 白名单验证）
  - 集成缓存查询/写入
- [ ] **T3.2** 实现 `tools/forecast.py` — `handle_get_forecast()` 函数：
  - 从原 `get_weather_forecast()` 迁移逻辑
  - **修复 hourly 数组索引越界 Bug**（添加 `safe_get_hourly()` 安全访问）
  - 添加输入参数二次校验
  - 集成缓存查询/写入

### 阶段 4：格式化与入口重构
- [ ] **T4.1** 实现 `formatters/weather.py`：
  - `format_current_weather()` — 格式化当前天气报告
  - `format_forecast()` — 格式化天气预报报告
  - 保持与原输出完全一致的 emoji 布局和文本结构
- [ ] **T4.2** 重构 `server.py` 入口：
  - 精简为 MCP 注册 + 路由分发（约 50 行）
  - 使用字典映射替代 if-elif 路由
  - 改进顶层错误处理（不暴露原始异常堆栈）

### 阶段 5：测试
- [ ] **T5.1** 编写 `tests/test_cache.py`：TTL 过期、容量驱逐、缓存命中/未命中
- [ ] **T5.2** 编写 `tests/test_weather_api.py`：URL 构造正确性、城市名编码、HTTP 错误处理（mock httpx）
- [ ] **T5.3** 编写 `tests/test_current.py`：数据解析、字段缺失处理、参数校验
- [ ] **T5.4** 编写 `tests/test_forecast.py`：多日预报解析、hourly 索引安全访问、不完整数据处理

### 阶段 6：收尾
- [ ] **T6.1** 运行全部测试，确保通过且覆盖率 ≥ 80%
- [ ] **T6.2** 更新 `README.md`：补充新的项目结构说明、环境变量配置文档
- [ ] **T6.3** 功能回归验证：启动重构后的服务，确认输入输出行为与重构前一致