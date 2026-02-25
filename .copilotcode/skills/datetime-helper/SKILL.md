---
name: datetime-helper
description: Comprehensive date and time processing skill. Use this skill when users need to: (1) Calculate time differences and durations, (2) Convert between time zones, (3) Format dates and times in various formats, (4) Parse date strings, (5) Perform date arithmetic (add/subtract days, months, years), (6) Get timestamps and Unix time, (7) Work with business days and holidays.
---

# DateTime Helper

## Overview

This skill provides comprehensive date and time processing capabilities, including time zone conversions, date calculations, formatting, parsing, and business day calculations.

## Core Capabilities

### 1. Time Zone Conversion

Use [`scripts/timezone_converter.py`](scripts/timezone_converter.py) for converting between different time zones:

```python
from scripts.timezone_converter import TimezoneConverter

converter = TimezoneConverter()

# Convert current time to different timezone
tokyo_time = converter.convert_to_timezone('Asia/Tokyo')
ny_time = converter.convert_to_timezone('America/New_York')

# Convert specific time between timezones
result = converter.convert_between_timezones(
    '2024-02-25 14:30:00',
    from_tz='America/Los_Angeles',
    to_tz='Europe/London'
)
```

### 2. Date Calculations

Use [`scripts/date_calculator.py`](scripts/date_calculator.py) for date arithmetic and calculations:

```python
from scripts.date_calculator import DateCalculator

calc = DateCalculator()

# Calculate time difference
diff = calc.time_difference('2024-01-01', '2024-12-31')  # Returns days, hours, etc.

# Add/subtract time periods
future_date = calc.add_days('2024-02-25', 30)
past_date = calc.subtract_months('2024-02-25', 3)

# Calculate age
age = calc.calculate_age('1990-05-15')

# Get date range
dates = calc.date_range('2024-02-01', '2024-02-29')
```

### 3. Date Formatting and Parsing

Use [`scripts/date_formatter.py`](scripts/date_formatter.py) for formatting and parsing dates:

```python
from scripts.date_formatter import DateFormatter

formatter = DateFormatter()

# Format dates in various ways
formatted = formatter.format_date('2024-02-25', format='%Y年%m月%d日')
iso_format = formatter.to_iso('2024-02-25 14:30:00')
human_readable = formatter.to_human_readable('2024-02-25')  # "February 25, 2024"

# Parse various date formats
parsed = formatter.parse_date('Feb 25, 2024')
parsed = formatter.parse_date('2024/02/25')
parsed = formatter.parse_date('25-02-2024')
```

### 4. Timestamp Operations

```python
from scripts.timestamp_helper import TimestampHelper

ts_helper = TimestampHelper()

# Get current timestamp
unix_ts = ts_helper.get_unix_timestamp()
iso_ts = ts_helper.get_iso_timestamp()

# Convert between timestamp formats
date_from_unix = ts_helper.unix_to_datetime(1708857600)
unix_from_date = ts_helper.datetime_to_unix('2024-02-25 14:30:00')

# Relative time
relative = ts_helper.get_relative_time('2024-02-20')  # "5 days ago"
```

### 5. Business Days and Holidays

Use [`scripts/business_days.py`](scripts/business_days.py) for working with business days:

```python
from scripts.business_days import BusinessDaysCalculator

business = BusinessDaysCalculator()

# Check if date is business day
is_business = business.is_business_day('2024-02-25')

# Calculate business days between dates
days = business.count_business_days('2024-02-01', '2024-02-29')

# Add business days
next_business_day = business.add_business_days('2024-02-25', 5)

# Get next/previous business day
next_day = business.next_business_day('2024-02-25')
```

## Workflow

### For Simple Date Operations

1. Use Python's built-in `datetime` module
2. Return the result directly

### For Complex Operations

1. Identify the operation type:
   - Timezone conversion → use [`scripts/timezone_converter.py`](scripts/timezone_converter.py)
   - Date calculations → use [`scripts/date_calculator.py`](scripts/date_calculator.py)
   - Formatting/parsing → use [`scripts/date_formatter.py`](scripts/date_formatter.py)
   - Business days → use [`scripts/business_days.py`](scripts/business_days.py)
2. Execute the operation
3. Present results clearly with context

### For Reference

Consult [`references/timezone_reference.md`](references/timezone_reference.md) for common timezone information and [`references/date_formats.md`](references/date_formats.md) for date format patterns.

## Best Practices

1. **Timezone Awareness**: Always specify timezone when dealing with specific times
2. **ISO 8601**: Prefer ISO 8601 format (YYYY-MM-DD) for dates
3. **Validation**: Validate date strings before parsing
4. **Error Handling**: Handle invalid dates and edge cases gracefully
5. **Localization**: Consider locale when formatting dates for users
6. **DST**: Be aware of Daylight Saving Time transitions

## Resources

### scripts/
- [`timezone_converter.py`](scripts/timezone_converter.py) - Timezone conversion utilities
- [`date_calculator.py`](scripts/date_calculator.py) - Date arithmetic and calculations
- [`date_formatter.py`](scripts/date_formatter.py) - Date formatting and parsing
- [`timestamp_helper.py`](scripts/timestamp_helper.py) - Timestamp operations
- [`business_days.py`](scripts/business_days.py) - Business day calculations

### references/
- [`timezone_reference.md`](references/timezone_reference.md) - Common timezone codes and information
- [`date_formats.md`](references/date_formats.md) - Date format patterns and examples

## Examples

### Example 1: Convert Meeting Time Across Timezones

```python
from scripts.timezone_converter import TimezoneConverter

converter = TimezoneConverter()

# Meeting at 9 AM PST, what time is it in Tokyo?
tokyo_time = converter.convert_between_timezones(
    '2024-02-25 09:00:00',
    from_tz='America/Los_Angeles',
    to_tz='Asia/Tokyo'
)
print(f"Meeting time in Tokyo: {tokyo_time}")
```

### Example 2: Calculate Project Duration

```python
from scripts.date_calculator import DateCalculator

calc = DateCalculator()

start_date = '2024-01-01'
end_date = '2024-02-25'

# Total days
total = calc.time_difference(start_date, end_date)
print(f"Project duration: {total['days']} days")

# Business days only
from scripts.business_days import BusinessDaysCalculator
business = BusinessDaysCalculator()
business_days = business.count_business_days(start_date, end_date)
print(f"Working days: {business_days}")
```

### Example 3: Format Dates for Different Locales

```python
from scripts.date_formatter import DateFormatter

formatter = DateFormatter()

date = '2024-02-25'

# Different formats
print(formatter.format_date(date, format='%Y-%m-%d'))  # 2024-02-25
print(formatter.format_date(date, format='%d/%m/%Y'))  # 25/02/2024
print(formatter.format_date(date, format='%B %d, %Y'))  # February 25, 2024
print(formatter.format_date(date, format='%Y年%m月%d日'))  # 2024年02月25日
```

### Example 4: Calculate Deadline with Business Days

```python
from scripts.business_days import BusinessDaysCalculator

business = BusinessDaysCalculator()

# Project starts today, needs 20 business days
start = '2024-02-25'
deadline = business.add_business_days(start, 20)
print(f"Project deadline: {deadline}")
```

## Common Use Cases

1. **Meeting Scheduling**: Convert meeting times across timezones
2. **Age Calculation**: Calculate age from birthdate
3. **Deadline Management**: Add business days to calculate deadlines
4. **Time Tracking**: Calculate time differences and durations
5. **Data Processing**: Parse and format dates from various sources
6. **Timestamp Conversion**: Convert between Unix timestamps and datetime
7. **Relative Time**: Display "3 days ago" or "in 2 hours"
