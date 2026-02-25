from datetime import datetime
import locale


class DateFormatter:
    """日期格式化工具类"""

    def __init__(self):
        """初始化日期格式化器"""
        pass

    def parse_date(self, date_str, fuzzy=True):
        """
        智能解析日期字符串

        参数:
            date_str (str): 日期字符串
            fuzzy (bool): 是否使用模糊解析

        返回:
            datetime: 解析后的日期对象
        """
        # 常见日期格式
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%Y年%m月%d日',
            '%m/%d/%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # 如果所有格式都失败，尝试使用 dateutil
        try:
            from dateutil import parser
            return parser.parse(date_str, fuzzy=fuzzy)
        except:
            raise ValueError(f"无法解析日期: {date_str}")

    def format_date(self, date, format='%Y-%m-%d'):
        """
        格式化日期

        参数:
            date (str or datetime): 日期
            format (str): 输出格式

        返回:
            str: 格式化后的日期字符串
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        return date.strftime(format)

    def to_iso(self, date):
        """
        转换为 ISO 8601 格式

        参数:
            date (str or datetime): 日期

        返回:
            str: ISO 格式的日期字符串
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        return date.isoformat()

    def to_human_readable(self, date, locale_name='en_US'):
        """
        转换为人类可读格式

        参数:
            date (str or datetime): 日期
            locale_name (str): 本地化名称

        返回:
            str: 人类可读的日期字符串
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        # 英文格式
        if locale_name == 'en_US':
            return date.strftime('%B %d, %Y')
        # 中文格式
        elif locale_name == 'zh_CN':
            return date.strftime('%Y年%m月%d日')
        # 默认格式
        else:
            return date.strftime('%d %B %Y')

    def to_relative_time(self, date):
        """
        转换为相对时间（例如："3 天前"）

        参数:
            date (str or datetime): 日期

        返回:
            str: 相对时间字符串
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        now = datetime.now()
        diff = now - date

        seconds = diff.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = diff.days
        weeks = days / 7
        months = days / 30
        years = days / 365

        if seconds < 60:
            return f"{int(seconds)} 秒前"
        elif minutes < 60:
            return f"{int(minutes)} 分钟前"
        elif hours < 24:
            return f"{int(hours)} 小时前"
        elif days < 7:
            return f"{int(days)} 天前"
        elif weeks < 4:
            return f"{int(weeks)} 周前"
        elif months < 12:
            return f"{int(months)} 个月前"
        else:
            return f"{int(years)} 年前"

    def get_common_formats(self, date):
        """
        获取常用格式列表

        参数:
            date (str or datetime): 日期

        返回:
            dict: 包含各种格式的字典
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        return {
            'iso': date.isoformat(),
            'standard': date.strftime('%Y-%m-%d'),
            'us': date.strftime('%m/%d/%Y'),
            'eu': date.strftime('%d/%m/%Y'),
            'full_text_en': date.strftime('%A, %B %d, %Y'),
            'full_text_short': date.strftime('%a, %b %d, %Y'),
            'chinese': date.strftime('%Y年%m月%d日'),
            'with_time': date.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': int(date.timestamp()),
            'relative': self.to_relative_time(date)
        }

    def format_time_range(self, start_date, end_date, format='%Y-%m-%d'):
        """
        格式化时间范围

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期
            format (str): 日期格式

        返回:
            str: 格式化的时间范围字符串
        """
        if isinstance(start_date, str):
            start_date = self.parse_date(start_date)
        if isinstance(end_date, str):
            end_date = self.parse_date(end_date)

        start_str = start_date.strftime(format)
        end_str = end_date.strftime(format)

        return f"{start_str} 至 {end_str}"

    def get_weekday_name(self, date, locale_name='en_US'):
        """
        获取星期名称

        参数:
            date (str or datetime): 日期
            locale_name (str): 本地化名称

        返回:
            str: 星期名称
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        weekdays_zh = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekdays_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        if locale_name == 'zh_CN':
            return weekdays_zh[date.weekday()]
        else:
            return weekdays_en[date.weekday()]

    def get_month_name(self, date, locale_name='en_US'):
        """
        获取月份名称

        参数:
            date (str or datetime): 日期
            locale_name (str): 本地化名称

        返回:
            str: 月份名称
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        months_zh = ['一月', '二月', '三月', '四月', '五月', '六月',
                     '七月', '八月', '九月', '十月', '十一月', '十二月']

        if locale_name == 'zh_CN':
            return months_zh[date.month - 1]
        else:
            return date.strftime('%B')

    def custom_format(self, date, template):
        """
        自定义格式化模板

        参数:
            date (str or datetime): 日期
            template (str): 模板字符串，支持占位符:
                {year} - 年份
                {month} - 月份
                {day} - 日期
                {weekday} - 星期
                {hour} - 小时
                {minute} - 分钟
                {second} - 秒

        返回:
            str: 格式化后的字符串
        """
        if isinstance(date, str):
            date = self.parse_date(date)

        replacements = {
            '{year}': str(date.year),
            '{month}': f'{date.month:02d}',
            '{day}': f'{date.day:02d}',
            '{weekday}': self.get_weekday_name(date, 'zh_CN'),
            '{hour}': f'{date.hour:02d}',
            '{minute}': f'{date.minute:02d}',
            '{second}': f'{date.second:02d}'
        }

        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)

        return result


# 示例使用
if __name__ == '__main__':
    formatter = DateFormatter()

    # 示例1: 解析各种日期格式
    dates = [
        '2024-02-25',
        '02/25/2024',
        'February 25, 2024',
        '2024年02月25日'
    ]
    print("Parsing various date formats:")
    for date_str in dates:
        parsed = formatter.parse_date(date_str)
        print(f"  {date_str} -> {parsed}")

    # 示例2: 获取常用格式
    print("\nCommon formats:")
    formats = formatter.get_common_formats('2024-02-25')
    for name, value in formats.items():
        print(f"  {name}: {value}")

    # 示例3: 自定义格式
    custom = formatter.custom_format('2024-02-25', '{year}年{month}月{day}日 {weekday}')
    print(f"\nCustom format: {custom}")

    # 示例4: 相对时间
    relative = formatter.to_relative_time('2024-02-20')
    print(f"\nRelative time: {relative}")
