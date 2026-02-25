from datetime import datetime, timedelta
import pytz


class TimezoneConverter:
    """时区转换工具类"""

    def __init__(self):
        """初始化时区转换器"""
        pass

    def get_all_timezones(self):
        """
        获取所有可用的时区列表

        返回:
            list: 时区名称列表
        """
        return pytz.all_timezones

    def convert_to_timezone(self, target_tz, dt=None, source_tz='UTC'):
        """
        将时间转换到目标时区

        参数:
            target_tz (str): 目标时区 (例如: 'Asia/Tokyo', 'America/New_York')
            dt (datetime): 要转换的时间，默认为当前时间
            source_tz (str): 源时区，默认为 UTC

        返回:
            datetime: 转换后的时间
        """
        if dt is None:
            dt = datetime.now(pytz.UTC)
        elif isinstance(dt, str):
            dt = datetime.fromisoformat(dt)

        # 如果没有时区信息，添加源时区
        if dt.tzinfo is None:
            source = pytz.timezone(source_tz)
            dt = source.localize(dt)

        # 转换到目标时区
        target = pytz.timezone(target_tz)
        converted = dt.astimezone(target)

        return converted

    def convert_between_timezones(self, dt_str, from_tz, to_tz):
        """
        在两个时区之间转换时间

        参数:
            dt_str (str): 时间字符串 (格式: 'YYYY-MM-DD HH:MM:SS')
            from_tz (str): 源时区
            to_tz (str): 目标时区

        返回:
            dict: 包含转换结果的字典
        """
        # 解析时间字符串
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

        # 设置源时区
        source_tz = pytz.timezone(from_tz)
        dt_with_tz = source_tz.localize(dt)

        # 转换到目标时区
        target_tz = pytz.timezone(to_tz)
        converted = dt_with_tz.astimezone(target_tz)

        return {
            'original': dt_with_tz.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'converted': converted.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'from_timezone': from_tz,
            'to_timezone': to_tz,
            'offset_hours': (converted.utcoffset().total_seconds() - dt_with_tz.utcoffset().total_seconds()) / 3600
        }

    def get_timezone_offset(self, tz_name, dt=None):
        """
        获取指定时区相对于 UTC 的偏移量

        参数:
            tz_name (str): 时区名称
            dt (datetime): 指定时间，默认为当前时间

        返回:
            dict: 包含偏移信息的字典
        """
        if dt is None:
            dt = datetime.now()

        tz = pytz.timezone(tz_name)
        localized = tz.localize(dt)
        offset = localized.utcoffset()

        return {
            'timezone': tz_name,
            'offset_hours': offset.total_seconds() / 3600,
            'offset_str': str(offset),
            'is_dst': bool(localized.dst())
        }

    def find_timezone_by_offset(self, offset_hours):
        """
        根据 UTC 偏移量查找时区

        参数:
            offset_hours (float): UTC 偏移小时数 (例如: 8 代表 UTC+8)

        返回:
            list: 匹配的时区列表
        """
        matching_timezones = []
        target_offset = timedelta(hours=offset_hours)

        for tz_name in pytz.common_timezones:
            tz = pytz.timezone(tz_name)
            dt = datetime.now(tz)
            if dt.utcoffset() == target_offset:
                matching_timezones.append(tz_name)

        return matching_timezones

    def get_common_timezones_info(self):
        """
        获取常用时区信息

        返回:
            dict: 常用时区及其当前时间
        """
        common_tz = [
            'UTC',
            'America/New_York',
            'America/Los_Angeles',
            'Europe/London',
            'Europe/Paris',
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Asia/Hong_Kong',
            'Australia/Sydney'
        ]

        result = {}
        for tz_name in common_tz:
            tz = pytz.timezone(tz_name)
            current_time = datetime.now(tz)
            result[tz_name] = {
                'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'offset': current_time.utcoffset().total_seconds() / 3600
            }

        return result


# 示例使用
if __name__ == '__main__':
    converter = TimezoneConverter()

    # 示例1: 转换当前时间到东京时区
    tokyo_time = converter.convert_to_timezone('Asia/Tokyo')
    print(f"Tokyo time: {tokyo_time}")

    # 示例2: 在时区之间转换
    result = converter.convert_between_timezones(
        '2024-02-25 14:30:00',
        from_tz='America/Los_Angeles',
        to_tz='Asia/Tokyo'
    )
    print(f"\nConversion result: {result}")

    # 示例3: 获取时区偏移量
    offset = converter.get_timezone_offset('Asia/Shanghai')
    print(f"\nShanghai offset: {offset}")

    # 示例4: 获取常用时区信息
    common_tz_info = converter.get_common_timezones_info()
    print(f"\nCommon timezones:")
    for tz, info in common_tz_info.items():
        print(f"  {tz}: {info['current_time']}")
