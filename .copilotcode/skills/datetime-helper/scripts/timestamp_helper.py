from datetime import datetime, timedelta


class TimestampHelper:
    """时间戳处理工具类"""

    def __init__(self):
        """初始化时间戳助手"""
        pass

    def get_unix_timestamp(self, dt=None):
        """
        获取 Unix 时间戳（秒）

        参数:
            dt (datetime): 日期时间对象，默认为当前时间

        返回:
            int: Unix 时间戳
        """
        if dt is None:
            dt = datetime.now()
        elif isinstance(dt, str):
            dt = datetime.fromisoformat(dt)

        return int(dt.timestamp())

    def get_unix_timestamp_ms(self, dt=None):
        """
        获取 Unix 时间戳（毫秒）

        参数:
            dt (datetime): 日期时间对象，默认为当前时间

        返回:
            int: Unix 时间戳（毫秒）
        """
        if dt is None:
            dt = datetime.now()
        elif isinstance(dt, str):
            dt = datetime.fromisoformat(dt)

        return int(dt.timestamp() * 1000)

    def get_iso_timestamp(self, dt=None):
        """
        获取 ISO 8601 格式的时间戳

        参数:
            dt (datetime): 日期时间对象，默认为当前时间

        返回:
            str: ISO 8601 格式的时间戳
        """
        if dt is None:
            dt = datetime.now()
        elif isinstance(dt, str):
            dt = datetime.fromisoformat(dt)

        return dt.isoformat()

    def unix_to_datetime(self, timestamp):
        """
        将 Unix 时间戳转换为 datetime 对象

        参数:
            timestamp (int or float): Unix 时间戳（秒或毫秒）

        返回:
            datetime: datetime 对象
        """
        # 如果是毫秒级时间戳，转换为秒
        if timestamp > 10000000000:
            timestamp = timestamp / 1000

        return datetime.fromtimestamp(timestamp)

    def unix_to_string(self, timestamp, format='%Y-%m-%d %H:%M:%S'):
        """
        将 Unix 时间戳转换为字符串

        参数:
            timestamp (int or float): Unix 时间戳
            format (str): 输出格式

        返回:
            str: 格式化的日期时间字符串
        """
        dt = self.unix_to_datetime(timestamp)
        return dt.strftime(format)

    def datetime_to_unix(self, dt_str):
        """
        将日期时间字符串转换为 Unix 时间戳

        参数:
            dt_str (str): 日期时间字符串

        返回:
            int: Unix 时间戳
        """
        # 尝试多种格式
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d'
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(dt_str, fmt)
                return int(dt.timestamp())
            except ValueError:
                continue

        # 如果都失败，尝试 ISO 格式
        try:
            dt = datetime.fromisoformat(dt_str)
            return int(dt.timestamp())
        except:
            raise ValueError(f"无法解析日期时间: {dt_str}")

    def get_relative_time(self, dt):
        """
        获取相对时间描述

        参数:
            dt (str or datetime or int): 日期时间或时间戳

        返回:
            str: 相对时间描述
        """
        # 处理不同类型的输入
        if isinstance(dt, int):
            dt = self.unix_to_datetime(dt)
        elif isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt)
            except:
                # 尝试作为时间戳解析
                try:
                    dt = self.unix_to_datetime(int(dt))
                except:
                    raise ValueError(f"无法解析输入: {dt}")

        now = datetime.now()
        diff = now - dt

        # 未来的时间
        if diff.total_seconds() < 0:
            diff = dt - now
            seconds = diff.total_seconds()
            minutes = seconds / 60
            hours = minutes / 60
            days = diff.days

            if seconds < 60:
                return f"{int(seconds)} 秒后"
            elif minutes < 60:
                return f"{int(minutes)} 分钟后"
            elif hours < 24:
                return f"{int(hours)} 小时后"
            elif days < 7:
                return f"{int(days)} 天后"
            elif days < 30:
                return f"{int(days / 7)} 周后"
            elif days < 365:
                return f"{int(days / 30)} 个月后"
            else:
                return f"{int(days / 365)} 年后"

        # 过去的时间
        seconds = diff.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = diff.days

        if seconds < 60:
            return f"{int(seconds)} 秒前"
        elif minutes < 60:
            return f"{int(minutes)} 分钟前"
        elif hours < 24:
            return f"{int(hours)} 小时前"
        elif days < 7:
            return f"{int(days)} 天前"
        elif days < 30:
            return f"{int(days / 7)} 周前"
        elif days < 365:
            return f"{int(days / 30)} 个月前"
        else:
            return f"{int(days / 365)} 年前"

    def timestamp_info(self, timestamp):
        """
        获取时间戳的详细信息

        参数:
            timestamp (int): Unix 时间戳

        返回:
            dict: 包含各种格式的时间信息
        """
        dt = self.unix_to_datetime(timestamp)

        return {
            'timestamp': timestamp,
            'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'iso': dt.isoformat(),
            'date': dt.strftime('%Y-%m-%d'),
            'time': dt.strftime('%H:%M:%S'),
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'weekday': dt.strftime('%A'),
            'relative': self.get_relative_time(timestamp)
        }

    def compare_timestamps(self, ts1, ts2):
        """
        比较两个时间戳

        参数:
            ts1 (int): 第一个时间戳
            ts2 (int): 第二个时间戳

        返回:
            dict: 比较结果
        """
        # 确保是秒级时间戳
        if ts1 > 10000000000:
            ts1 = ts1 / 1000
        if ts2 > 10000000000:
            ts2 = ts2 / 1000

        diff = abs(ts2 - ts1)
        dt1 = self.unix_to_datetime(ts1)
        dt2 = self.unix_to_datetime(ts2)

        return {
            'timestamp1': int(ts1),
            'timestamp2': int(ts2),
            'datetime1': dt1.strftime('%Y-%m-%d %H:%M:%S'),
            'datetime2': dt2.strftime('%Y-%m-%d %H:%M:%S'),
            'difference_seconds': int(diff),
            'difference_minutes': diff / 60,
            'difference_hours': diff / 3600,
            'difference_days': diff / 86400,
            'earlier': 'timestamp1' if ts1 < ts2 else 'timestamp2'
        }

    def get_timestamp_ranges(self, reference_time=None):
        """
        获取常用的时间戳范围

        参数:
            reference_time (datetime): 参考时间，默认为当前时间

        返回:
            dict: 包含各种时间范围的时间戳
        """
        if reference_time is None:
            reference_time = datetime.now()

        # 今天的开始和结束
        today_start = reference_time.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = reference_time.replace(hour=23, minute=59, second=59, microsecond=999999)

        # 昨天
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end = today_end - timedelta(days=1)

        # 本周
        week_start = today_start - timedelta(days=today_start.weekday())
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        # 本月
        month_start = reference_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if reference_time.month == 12:
            month_end = month_start.replace(year=reference_time.year + 1, month=1) - timedelta(seconds=1)
        else:
            month_end = month_start.replace(month=reference_time.month + 1) - timedelta(seconds=1)

        return {
            'now': int(reference_time.timestamp()),
            'today_start': int(today_start.timestamp()),
            'today_end': int(today_end.timestamp()),
            'yesterday_start': int(yesterday_start.timestamp()),
            'yesterday_end': int(yesterday_end.timestamp()),
            'week_start': int(week_start.timestamp()),
            'week_end': int(week_end.timestamp()),
            'month_start': int(month_start.timestamp()),
            'month_end': int(month_end.timestamp())
        }


# 示例使用
if __name__ == '__main__':
    helper = TimestampHelper()

    # 示例1: 获取当前时间戳
    current_ts = helper.get_unix_timestamp()
    print(f"Current timestamp: {current_ts}")

    # 示例2: 时间戳转换为日期时间
    dt_str = helper.unix_to_string(current_ts)
    print(f"Timestamp to string: {dt_str}")

    # 示例3: 日期时间转换为时间戳
    ts = helper.datetime_to_unix('2024-02-25 14:30:00')
    print(f"String to timestamp: {ts}")

    # 示例4: 获取相对时间
    relative = helper.get_relative_time(current_ts - 3600)
    print(f"Relative time: {relative}")

    # 示例5: 获取时间戳详细信息
    info = helper.timestamp_info(current_ts)
    print(f"\nTimestamp info:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    # 示例6: 获取时间戳范围
    ranges = helper.get_timestamp_ranges()
    print(f"\nTimestamp ranges:")
    for key, value in ranges.items():
        print(f"  {key}: {value}")
