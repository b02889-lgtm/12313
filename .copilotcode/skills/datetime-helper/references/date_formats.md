# Date Format Patterns

## Python strftime/strptime Directives

### Year
- `%Y` - Year with century (e.g., 2024)
- `%y` - Year without century (e.g., 24)

### Month
- `%m` - Month as zero-padded number (01-12)
- `%B` - Full month name (e.g., February)
- `%b` - Abbreviated month name (e.g., Feb)

### Day
- `%d` - Day of month as zero-padded number (01-31)
- `%j` - Day of year as zero-padded number (001-366)
- `%A` - Full weekday name (e.g., Monday)
- `%a` - Abbreviated weekday name (e.g., Mon)
- `%w` - Weekday as number (0=Sunday, 6=Saturday)
- `%u` - Weekday as number (1=Monday, 7=Sunday)

### Time
- `%H` - Hour (24-hour clock) as zero-padded number (00-23)
- `%I` - Hour (12-hour clock) as zero-padded number (01-12)
- `%M` - Minute as zero-padded number (00-59)
- `%S` - Second as zero-padded number (00-59)
- `%f` - Microsecond as zero-padded number (000000-999999)
- `%p` - AM/PM

### Timezone
- `%z` - UTC offset (+0000, -0400, +0530)
- `%Z` - Timezone name (EST, PST, etc.)

### Other
- `%%` - Literal '%' character

## Common Format Patterns

### ISO 8601 (International Standard)
```
%Y-%m-%d                    # 2024-02-25
%Y-%m-%dT%H:%M:%S           # 2024-02-25T14:30:00
%Y-%m-%dT%H:%M:%S%z         # 2024-02-25T14:30:00+0800
%Y-%m-%dT%H:%M:%S.%f        # 2024-02-25T14:30:00.123456
```

### US Format
```
%m/%d/%Y                    # 02/25/2024
%m/%d/%y                    # 02/25/24
%B %d, %Y                   # February 25, 2024
%b %d, %Y                   # Feb 25, 2024
%m-%d-%Y                    # 02-25-2024
```

### European Format
```
%d/%m/%Y                    # 25/02/2024
%d/%m/%y                    # 25/02/24
%d-%m-%Y                    # 25-02-2024
%d.%m.%Y                    # 25.02.2024
%d %B %Y                    # 25 February 2024
%d %b %Y                    # 25 Feb 2024
```

### Chinese Format
```
%Y年%m月%d日                 # 2024年02月25日
%Y年%m月%d日 %H:%M:%S        # 2024年02月25日 14:30:00
%Y-%m-%d %H时%M分%S秒        # 2024-02-25 14时30分00秒
```

### Time Only
```
%H:%M:%S                    # 14:30:00
%H:%M                       # 14:30
%I:%M %p                    # 02:30 PM
%I:%M:%S %p                 # 02:30:00 PM
```

### Full Date and Time
```
%Y-%m-%d %H:%M:%S           # 2024-02-25 14:30:00
%d/%m/%Y %H:%M:%S           # 25/02/2024 14:30:00
%A, %B %d, %Y %I:%M %p      # Sunday, February 25, 2024 02:30 PM
%a, %d %b %Y %H:%M:%S %Z    # Sun, 25 Feb 2024 14:30:00 CST
```

### RFC 2822 (Email Format)
```
%a, %d %b %Y %H:%M:%S %z    # Sun, 25 Feb 2024 14:30:00 +0800
```

### RFC 3339 (Internet Date/Time)
```
%Y-%m-%dT%H:%M:%S%z         # 2024-02-25T14:30:00+08:00
```

## Examples by Use Case

### Database Formats
```python
# MySQL DATETIME
'%Y-%m-%d %H:%M:%S'         # 2024-02-25 14:30:00

# PostgreSQL TIMESTAMP
'%Y-%m-%d %H:%M:%S'         # 2024-02-25 14:30:00

# SQLite
'%Y-%m-%d %H:%M:%S'         # 2024-02-25 14:30:00
```

### Log Formats
```python
# Standard log format
'%Y-%m-%d %H:%M:%S'         # 2024-02-25 14:30:00

# Apache log format
'%d/%b/%Y:%H:%M:%S %z'      # 25/Feb/2024:14:30:00 +0800

# Syslog format
'%b %d %H:%M:%S'            # Feb 25 14:30:00
```

### Filename Formats
```python
# Date-based filename
'%Y%m%d'                    # 20240225

# With timestamp
'%Y%m%d_%H%M%S'             # 20240225_143000

# Human readable
'%Y-%m-%d_%H-%M-%S'         # 2024-02-25_14-30-00
```

### Display Formats
```python
# Short date
'%Y-%m-%d'                  # 2024-02-25
'%m/%d/%Y'                  # 02/25/2024
'%d/%m/%Y'                  # 25/02/2024

# Long date
'%B %d, %Y'                 # February 25, 2024
'%A, %B %d, %Y'             # Sunday, February 25, 2024

# With time
'%B %d, %Y at %I:%M %p'     # February 25, 2024 at 02:30 PM
```

## Localization Examples

### English (US)
```python
'%m/%d/%Y'                  # 02/25/2024
'%B %d, %Y'                 # February 25, 2024
'%I:%M %p'                  # 02:30 PM
```

### English (UK)
```python
'%d/%m/%Y'                  # 25/02/2024
'%d %B %Y'                  # 25 February 2024
'%H:%M'                     # 14:30
```

### Chinese
```python
'%Y年%m月%d日'               # 2024年02月25日
'%Y年%m月%d日 %H:%M'         # 2024年02月25日 14:30
```

### Japanese
```python
'%Y年%m月%d日'               # 2024年02月25日
'%Y/%m/%d'                  # 2024/02/25
```

### German
```python
'%d.%m.%Y'                  # 25.02.2024
'%d. %B %Y'                 # 25. Februar 2024
```

### French
```python
'%d/%m/%Y'                  # 25/02/2024
'%d %B %Y'                  # 25 février 2024
```

## Quick Reference Table

| Format | Example Output | Description |
|--------|----------------|-------------|
| `%Y-%m-%d` | 2024-02-25 | ISO 8601 date |
| `%m/%d/%Y` | 02/25/2024 | US date format |
| `%d/%m/%Y` | 25/02/2024 | European date format |
| `%B %d, %Y` | February 25, 2024 | Full month name |
| `%b %d, %Y` | Feb 25, 2024 | Abbreviated month |
| `%Y年%m月%d日` | 2024年02月25日 | Chinese format |
| `%H:%M:%S` | 14:30:00 | 24-hour time |
| `%I:%M %p` | 02:30 PM | 12-hour time with AM/PM |
| `%Y-%m-%d %H:%M:%S` | 2024-02-25 14:30:00 | Full datetime |
| `%Y-%m-%dT%H:%M:%S%z` | 2024-02-25T14:30:00+0800 | ISO 8601 with timezone |

## Best Practices

1. **Use ISO 8601 for storage**: `%Y-%m-%d` or `%Y-%m-%dT%H:%M:%S%z`
2. **Localize for display**: Use appropriate format for user's locale
3. **Be consistent**: Use the same format throughout your application
4. **Include timezone**: When time is important, always include timezone info
5. **Avoid ambiguity**: Prefer formats that are unambiguous (e.g., ISO 8601 over `%m/%d/%Y`)
6. **Document formats**: Always document which format you're using

## Common Parsing Pitfalls

### Ambiguous Formats
```python
# Ambiguous: could be Feb 3 or March 2
'02/03/2024'

# Better: use ISO format
'2024-02-03'  # Clearly February 3rd
```

### Missing Leading Zeros
```python
# May fail to parse
'2024-2-5'

# Better: use zero-padded
'2024-02-05'
```

### Timezone Confusion
```python
# No timezone info - ambiguous
'2024-02-25 14:30:00'

# Better: include timezone
'2024-02-25 14:30:00+08:00'
```
