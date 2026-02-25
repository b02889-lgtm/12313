from datetime import datetime, timedelta
import calendar


class BusinessDaysCalculator:
    """工作日计算工具类"""

    def __init__(self, holidays=None, workdays=None):
        """
        初始化工作日计算器

        参数:
            holidays (list): 节假日列表（日期字符串），默认为空
            workdays (list): 工作日索引列表（0=周一，6=周日），默认为周一到周五
        """
        self.holidays = set(holidays) if holidays else set()
        self.workdays = workdays if workdays else [0, 1, 2, 3, 4]  # 默认周一到周五

    def parse_date(self, date_input):
        """
        解析日期输入

        参数:
            date_input (str or datetime): 日期字符串或 datetime 对象

        返回:
            datetime: 解析后的日期对象
        """
        if isinstance(date_input, datetime):
            return date_input
        elif isinstance(date_input, str):
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_input, fmt)
                except ValueError:
                    continue
            raise ValueError(f"无法解析日期: {date_input}")
        else:
            raise TypeError("日期必须是字符串或 datetime 对象")

    def add_holiday(self, date):
        """
        添加节假日

        参数:
            date (str): 节假日日期
        """
        self.holidays.add(date)

    def remove_holiday(self, date):
        """
        移除节假日

        参数:
            date (str): 节假日日期
        """
        self.holidays.discard(date)

    def set_holidays(self, holidays):
        """
        设置节假日列表

        参数:
            holidays (list): 节假日列表
        """
        self.holidays = set(holidays)

    def is_weekend(self, date):
        """
        判断是否为周末

        参数:
            date (str or datetime): 日期

        返回:
            bool: 是否为周末
        """
        dt = self.parse_date(date)
        return dt.weekday() not in self.workdays

    def is_holiday(self, date):
        """
        判断是否为节假日

        参数:
            date (str or datetime): 日期

        返回:
            bool: 是否为节假日
        """
        dt = self.parse_date(date)
        date_str = dt.strftime('%Y-%m-%d')
        return date_str in self.holidays

    def is_business_day(self, date):
        """
        判断是否为工作日

        参数:
            date (str or datetime): 日期

        返回:
            bool: 是否为工作日
        """
        return not self.is_weekend(date) and not self.is_holiday(date)

    def next_business_day(self, date):
        """
        获取下一个工作日

        参数:
            date (str or datetime): 基准日期

        返回:
            str: 下一个工作日
        """
        dt = self.parse_date(date)
        next_day = dt + timedelta(days=1)

        while not self.is_business_day(next_day):
            next_day += timedelta(days=1)

        return next_day.strftime('%Y-%m-%d')

    def previous_business_day(self, date):
        """
        获取前一个工作日

        参数:
            date (str or datetime): 基准日期

        返回:
            str: 前一个工作日
        """
        dt = self.parse_date(date)
        prev_day = dt - timedelta(days=1)

        while not self.is_business_day(prev_day):
            prev_day -= timedelta(days=1)

        return prev_day.strftime('%Y-%m-%d')

    def add_business_days(self, date, days):
        """
        添加工作日

        参数:
            date (str or datetime): 基准日期
            days (int): 要添加的工作日数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        added_days = 0

        while added_days < days:
            dt += timedelta(days=1)
            if self.is_business_day(dt):
                added_days += 1

        return dt.strftime('%Y-%m-%d')

    def subtract_business_days(self, date, days):
        """
        减去工作日

        参数:
            date (str or datetime): 基准日期
            days (int): 要减去的工作日数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        subtracted_days = 0

        while subtracted_days < days:
            dt -= timedelta(days=1)
            if self.is_business_day(dt):
                subtracted_days += 1

        return dt.strftime('%Y-%m-%d')

    def count_business_days(self, start_date, end_date):
        """
        计算两个日期之间的工作日数

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期

        返回:
            int: 工作日数
        """
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)

        # 确保 start 在 end 之前
        if start > end:
            start, end = end, start

        business_days = 0
        current = start

        while current <= end:
            if self.is_business_day(current):
                business_days += 1
            current += timedelta(days=1)

        return business_days

    def get_business_days_in_month(self, year, month):
        """
        获取指定月份的工作日数

        参数:
            year (int): 年份
            month (int): 月份

        返回:
            dict: 包含工作日信息的字典
        """
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        business_days = self.count_business_days(first_day, last_day)
        total_days = calendar.monthrange(year, month)[1]

        return {
            'year': year,
            'month': month,
            'total_days': total_days,
            'business_days': business_days,
            'weekend_days': total_days - business_days - len([h for h in self.holidays if h.startswith(f'{year}-{month:02d}')]),
            'holidays': len([h for h in self.holidays if h.startswith(f'{year}-{month:02d}')])
        }

    def get_business_days_list(self, start_date, end_date):
        """
        获取日期范围内的所有工作日列表

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期

        返回:
            list: 工作日列表
        """
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)

        business_days = []
        current = start

        while current <= end:
            if self.is_business_day(current):
                business_days.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

        return business_days

    def get_weekend_days_list(self, start_date, end_date):
        """
        获取日期范围内的所有周末列表

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期

        返回:
            list: 周末日期列表
        """
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)

        weekend_days = []
        current = start

        while current <= end:
            if self.is_weekend(current):
                weekend_days.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

        return weekend_days

    @staticmethod
    def get_chinese_holidays(year):
        """
        获取中国法定节假日（简化版，仅供参考）

        参数:
            year (int): 年份

        返回:
            list: 节假日列表
        """
        # 注意：这是一个简化版本，实际节假日需要根据国务院公告确定
        # 这里只列出固定日期的节假日
        holidays = [
            f'{year}-01-01',  # 元旦
            f'{year}-05-01',  # 劳动节
            f'{year}-10-01',  # 国庆节
            f'{year}-10-02',
            f'{year}-10-03',
        ]
        return holidays


# 示例使用
if __name__ == '__main__':
    # 创建工作日计算器，添加一些节假日
    holidays = ['2024-01-01', '2024-05-01', '2024-10-01']
    calc = BusinessDaysCalculator(holidays=holidays)

    # 示例1: 判断是否为工作日
    print(f"2024-02-25 is business day: {calc.is_business_day('2024-02-25')}")
    print(f"2024-02-24 is business day: {calc.is_business_day('2024-02-24')}")  # 周六

    # 示例2: 获取下一个工作日
    next_bd = calc.next_business_day('2024-02-23')  # 周五
    print(f"\nNext business day after 2024-02-23: {next_bd}")

    # 示例3: 添加工作日
    future = calc.add_business_days('2024-02-25', 10)
    print(f"\n10 business days from 2024-02-25: {future}")

    # 示例4: 计算工作日数
    business_days = calc.count_business_days('2024-02-01', '2024-02-29')
    print(f"\nBusiness days in Feb 2024: {business_days}")

    # 示例5: 获取月份工作日信息
    month_info = calc.get_business_days_in_month(2024, 2)
    print(f"\nFebruary 2024 info: {month_info}")

    # 示例6: 获取工作日列表
    bd_list = calc.get_business_days_list('2024-02-20', '2024-02-29')
    print(f"\nBusiness days list: {bd_list}")
