# DateTime Helper Skill

一个全面的日期时间处理技能，提供时区转换、日期计算、格式化、时间戳操作和工作日计算等功能。

## 功能概览

### 1. 时区转换 (Timezone Converter)
- 在不同时区之间转换时间
- 获取时区偏移量
- 查找特定 UTC 偏移的时区
- 获取常用时区的当前时间

### 2. 日期计算 (Date Calculator)
- 计算两个日期之间的时间差
- 添加/减去天数、月数、年数
- 计算年龄
- 生成日期范围
- 获取月份和季度信息

### 3. 日期格式化 (Date Formatter)
- 智能解析多种日期格式
- 格式化日期为各种格式
- 转换为 ISO 8601 格式
- 生成人类可读的日期
- 相对时间显示（"3天前"）

### 4. 时间戳操作 (Timestamp Helper)
- 获取 Unix 时间戳（秒/毫秒）
- 时间戳和日期时间互相转换
- 相对时间描述
- 时间戳详细信息
- 时间戳范围生成

### 5. 工作日计算 (Business Days)
- 判断是否为工作日
- 计算工作日数量
- 添加/减去工作日
- 获取下一个/前一个工作日
- 自定义节假日设置

## 快速开始

### 安装依赖

```bash
pip install pytz python-dateutil
```

### 基本使用

#### 时区转换
```python
from scripts.timezone_converter import TimezoneConverter

converter = TimezoneConverter()

# 将时间转换到东京时区
tokyo_time = converter.convert_to_timezone('Asia/Tokyo')

# 在两个时区之间转换
result = converter.convert_between_timezones(
    '2024-02-25 14:30:00',
    from_tz='America/Los_Angeles',
    to_tz='Asia/Tokyo'
)
```

#### 日期计算
```python
from scripts.date_calculator import DateCalculator

calc = DateCalculator()

# 计算时间差
diff = calc.time_difference('2024-01-01', '2024-12-31')

# 添加30天
future = calc.add_days('2024-02-25', 30)

# 计算年龄
age = calc.calculate_age('1990-05-15')
```

#### 日期格式化
```python
from scripts.date_formatter import DateFormatter

formatter = DateFormatter()

# 解析日期
parsed = formatter.parse_date('Feb 25, 2024')

# 格式化日期
formatted = formatter.format_date('2024-02-25', format='%Y年%m月%d日')

# 获取相对时间
relative = formatter.to_relative_time('2024-02-20')  # "5天前"
```

#### 时间戳操作
```python
from scripts.timestamp_helper import TimestampHelper

helper = TimestampHelper()

# 获取当前时间戳
timestamp = helper.get_unix_timestamp()

# 时间戳转日期
date_str = helper.unix_to_string(1708857600)

# 日期转时间戳
timestamp = helper.datetime_to_unix('2024-02-25 14:30:00')
```

#### 工作日计算
```python
from scripts.business_days import BusinessDaysCalculator

# 设置节假日
holidays = ['2024-01-01', '2024-05-01', '2024-10-01']
calc = BusinessDaysCalculator(holidays=holidays)

# 判断是否为工作日
is_business = calc.is_business_day('2024-02-25')

# 添加10个工作日
deadline = calc.add_business_days('2024-02-25', 10)

# 计算工作日数
business_days = calc.count_business_days('2024-02-01', '2024-02-29')
```

## 使用场景

### 场景 1: 跨时区会议安排
```python
from scripts.timezone_converter import TimezoneConverter

converter = TimezoneConverter()

# 太平洋时间上午9点，在东京是几点？
meeting_time = converter.convert_between_timezones(
    '2024-02-25 09:00:00',
    from_tz='America/Los_Angeles',
    to_tz='Asia/Tokyo'
)
print(f"东京时间: {meeting_time['converted']}")
```

### 场景 2: 项目截止日期计算
```python
from scripts.business_days import BusinessDaysCalculator

calc = BusinessDaysCalculator()

# 项目需要20个工作日完成
start_date = '2024-02-25'
deadline = calc.add_business_days(start_date, 20)
print(f"项目截止日期: {deadline}")
```

### 场景 3: 生日倒计时
```python
from scripts.date_calculator import DateCalculator

calc = DateCalculator()

# 计算距离生日还有多少天
birthday = '2024-12-25'
diff = calc.time_difference('2024-02-25', birthday)
print(f"距离生日还有 {diff['days']} 天")
```

### 场景 4: 日志时间格式化
```python
from scripts.timestamp_helper import TimestampHelper

helper = TimestampHelper()

# 将日志中的时间戳转换为可读格式
log_timestamp = 1708857600
readable_time = helper.unix_to_string(log_timestamp, format='%Y-%m-%d %H:%M:%S')
relative_time = helper.get_relative_time(log_timestamp)
print(f"时间: {readable_time} ({relative_time})")
```

## 目录结构

```
datetime-helper/
├── SKILL.md                          # Skill 说明文档
├── README.md                         # 本文件
├── scripts/                          # 脚本文件夹
│   ├── timezone_converter.py        # 时区转换
│   ├── date_calculator.py           # 日期计算
│   ├── date_formatter.py            # 日期格式化
│   ├── timestamp_helper.py          # 时间戳操作
│   └── business_days.py             # 工作日计算
└── references/                       # 参考文档
    ├── timezone_reference.md        # 时区参考
    └── date_formats.md              # 日期格式参考
```

## 依赖项

- Python 3.6+
- pytz: 时区处理
- python-dateutil: 日期解析和相对时间计算

## 最佳实践

1. **时区意识**: 处理具体时间时，始终指定时区
2. **ISO 8601**: 优先使用 ISO 8601 格式 (YYYY-MM-DD) 存储日期
3. **验证输入**: 解析日期前先验证日期字符串
4. **错误处理**: 优雅地处理无效日期和边界情况
5. **本地化**: 为用户格式化日期时考虑本地化
6. **夏令时**: 注意夏令时转换

## 参考资源

- [时区参考](references/timezone_reference.md) - 常用时区代码和信息
- [日期格式参考](references/date_formats.md) - 日期格式模式和示例
- [IANA 时区数据库](https://www.iana.org/time-zones)
- [Python datetime 文档](https://docs.python.org/3/library/datetime.html)

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License
