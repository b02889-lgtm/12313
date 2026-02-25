# Timezone Reference

## Common Timezones

### Americas
- **UTC-8**: `America/Los_Angeles` (PST/PDT - Pacific Time)
- **UTC-7**: `America/Denver` (MST/MDT - Mountain Time)
- **UTC-6**: `America/Chicago` (CST/CDT - Central Time)
- **UTC-5**: `America/New_York` (EST/EDT - Eastern Time)
- **UTC-3**: `America/Sao_Paulo` (BRT - Brazil Time)

### Europe
- **UTC+0**: `Europe/London` (GMT/BST - British Time)
- **UTC+1**: `Europe/Paris`, `Europe/Berlin`, `Europe/Rome` (CET/CEST - Central European Time)
- **UTC+2**: `Europe/Helsinki`, `Europe/Athens` (EET/EEST - Eastern European Time)
- **UTC+3**: `Europe/Moscow` (MSK - Moscow Time)

### Asia
- **UTC+5:30**: `Asia/Kolkata` (IST - India Standard Time)
- **UTC+7**: `Asia/Bangkok`, `Asia/Jakarta` (ICT - Indochina Time)
- **UTC+8**: `Asia/Shanghai`, `Asia/Hong_Kong`, `Asia/Singapore` (CST - China Standard Time)
- **UTC+9**: `Asia/Tokyo`, `Asia/Seoul` (JST/KST - Japan/Korea Standard Time)

### Pacific
- **UTC+10**: `Australia/Sydney`, `Australia/Melbourne` (AEST/AEDT - Australian Eastern Time)
- **UTC+12**: `Pacific/Auckland` (NZST/NZDT - New Zealand Time)

### Other
- **UTC+0**: `UTC`, `GMT` (Coordinated Universal Time / Greenwich Mean Time)

## Timezone Abbreviations

### North America
- **PST**: Pacific Standard Time (UTC-8)
- **PDT**: Pacific Daylight Time (UTC-7)
- **MST**: Mountain Standard Time (UTC-7)
- **MDT**: Mountain Daylight Time (UTC-6)
- **CST**: Central Standard Time (UTC-6)
- **CDT**: Central Daylight Time (UTC-5)
- **EST**: Eastern Standard Time (UTC-5)
- **EDT**: Eastern Daylight Time (UTC-4)

### Europe
- **GMT**: Greenwich Mean Time (UTC+0)
- **BST**: British Summer Time (UTC+1)
- **CET**: Central European Time (UTC+1)
- **CEST**: Central European Summer Time (UTC+2)
- **EET**: Eastern European Time (UTC+2)
- **EEST**: Eastern European Summer Time (UTC+3)

### Asia
- **CST**: China Standard Time (UTC+8)
- **JST**: Japan Standard Time (UTC+9)
- **KST**: Korea Standard Time (UTC+9)
- **IST**: India Standard Time (UTC+5:30)
- **SGT**: Singapore Time (UTC+8)
- **HKT**: Hong Kong Time (UTC+8)

### Pacific
- **AEST**: Australian Eastern Standard Time (UTC+10)
- **AEDT**: Australian Eastern Daylight Time (UTC+11)
- **NZST**: New Zealand Standard Time (UTC+12)
- **NZDT**: New Zealand Daylight Time (UTC+13)

## Daylight Saving Time (DST)

### Regions that Observe DST
- Most of North America (except Arizona, Hawaii)
- Most of Europe
- Parts of Australia and New Zealand
- Some regions in Middle East and South America

### Regions that Do NOT Observe DST
- Most of Asia (China, Japan, India, Singapore, etc.)
- Most of Africa
- Parts of Australia (Queensland, Northern Territory, Western Australia)
- Arizona and Hawaii (USA)

### DST Transition Dates (Typical)
- **North America**: Second Sunday in March (spring forward), First Sunday in November (fall back)
- **Europe**: Last Sunday in March (spring forward), Last Sunday in October (fall back)
- **Australia**: First Sunday in October (spring forward), First Sunday in April (fall back)

## Timezone Offset Examples

### Positive Offsets (East of UTC)
```
UTC+1:   Europe/Paris
UTC+2:   Europe/Athens
UTC+3:   Europe/Moscow
UTC+5:30: Asia/Kolkata
UTC+8:   Asia/Shanghai
UTC+9:   Asia/Tokyo
UTC+12:  Pacific/Auckland
```

### Negative Offsets (West of UTC)
```
UTC-5:  America/New_York
UTC-6:  America/Chicago
UTC-7:  America/Denver
UTC-8:  America/Los_Angeles
UTC-10: Pacific/Honolulu
```

## Common Time Conversions

### When it's 12:00 PM (noon) UTC:
- **Los Angeles**: 4:00 AM (PST)
- **New York**: 7:00 AM (EST)
- **London**: 12:00 PM (GMT)
- **Paris**: 1:00 PM (CET)
- **Dubai**: 4:00 PM (GST)
- **Shanghai**: 8:00 PM (CST)
- **Tokyo**: 9:00 PM (JST)
- **Sydney**: 11:00 PM (AEDT, with DST)

## Best Practices

1. **Always Store in UTC**: Store timestamps in UTC in databases
2. **Convert for Display**: Convert to user's local timezone only for display
3. **Use IANA Names**: Use full IANA timezone names (e.g., `America/New_York`) instead of abbreviations
4. **Handle DST**: Be aware of DST transitions when calculating time differences
5. **Test Edge Cases**: Test timezone conversions around DST transition dates
6. **User Preferences**: Allow users to set their preferred timezone

## Useful Links

- IANA Time Zone Database: https://www.iana.org/time-zones
- Time Zone Converter: https://www.timeanddate.com/worldclock/converter.html
- Current time in all timezones: https://www.timeanddate.com/worldclock/

## Python Libraries

### pytz
```python
import pytz
from datetime import datetime

# Get timezone
tz = pytz.timezone('Asia/Shanghai')

# Localize time
dt = datetime(2024, 2, 25, 14, 30)
localized = tz.localize(dt)

# Convert timezone
tokyo_tz = pytz.timezone('Asia/Tokyo')
tokyo_time = localized.astimezone(tokyo_tz)
```

### dateutil
```python
from dateutil import tz
from datetime import datetime

# Get timezone
shanghai_tz = tz.gettz('Asia/Shanghai')
tokyo_tz = tz.gettz('Asia/Tokyo')

# Create time with timezone
dt = datetime(2024, 2, 25, 14, 30, tzinfo=shanghai_tz)

# Convert timezone
tokyo_time = dt.astimezone(tokyo_tz)
```
