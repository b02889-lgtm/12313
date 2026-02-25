from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


class DateCalculator:
    """日期计算工具类"""

    def __init__(self):
        """初始化日期计算器"""
        pass

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
            # 尝试多种常见格式
            formats = [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%d-%m-%Y',
                '%d/%m/%Y',
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d %H:%M:%S'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_input, fmt)
                except ValueError:
                    continue
            raise ValueError(f"无法解析日期: {date_input}")
        else:
            raise TypeError("日期必须是字符串或 datetime 对象")

    def time_difference(self, start_date, end_date):
        """
        计算两个日期之间的时间差

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期

        返回:
            dict: 包含天数、小时数等的字典
        """
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)
        diff = end - start

        return {
            'days': diff.days,
            'total_seconds': diff.total_seconds(),
            'hours': diff.total_seconds() / 3600,
            'minutes': diff.total_seconds() / 60,
            'weeks': diff.days / 7,
            'formatted': str(diff)
        }

    def add_days(self, date, days):
        """
        添加天数

        参数:
            date (str or datetime): 基准日期
            days (int): 要添加的天数

        返回:
            datetime: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt + timedelta(days=days)
        return result.strftime('%Y-%m-%d')

    def subtract_days(self, date, days):
        """
        减去天数

        参数:
            date (str or datetime): 基准日期
            days (int): 要减去的天数

        返回:
            datetime: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt - timedelta(days=days)
        return result.strftime('%Y-%m-%d')

    def add_months(self, date, months):
        """
        添加月数

        参数:
            date (str or datetime): 基准日期
            months (int): 要添加的月数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt + relativedelta(months=months)
        return result.strftime('%Y-%m-%d')

    def subtract_months(self, date, months):
        """
        减去月数

        参数:
            date (str or datetime): 基准日期
            months (int): 要减去的月数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt - relativedelta(months=months)
        return result.strftime('%Y-%m-%d')

    def add_years(self, date, years):
        """
        添加年数

        参数:
            date (str or datetime): 基准日期
            years (int): 要添加的年数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt + relativedelta(years=years)
        return result.strftime('%Y-%m-%d')

    def subtract_years(self, date, years):
        """
        减去年数

        参数:
            date (str or datetime): 基准日期
            years (int): 要减去的年数

        返回:
            str: 计算后的日期
        """
        dt = self.parse_date(date)
        result = dt - relativedelta(years=years)
        return result.strftime('%Y-%m-%d')

    def calculate_age(self, birthdate, reference_date=None):
        """
        计算年龄

        参数:
            birthdate (str or datetime): 出生日期
            reference_date (str or datetime): 参考日期，默认为今天

        返回:
            dict: 包含年龄信息的字典
        """
        birth = self.parse_date(birthdate)
        if reference_date is None:
            reference = datetime.now()
        else:
            reference = self.parse_date(reference_date)

        age = relativedelta(reference, birth)

        return {
            'years': age.years,
            'months': age.months,
            'days': age.days,
            'total_days': (reference - birth).days,
            'formatted': f"{age.years} 岁 {age.months} 个月 {age.days} 天"
        }

    def date_range(self, start_date, end_date, step_days=1):
        """
        生成日期范围

        参数:
            start_date (str or datetime): 开始日期
            end_date (str or datetime): 结束日期
            step_days (int): 步长（天数），默认为1

        返回:
            list: 日期列表
        """
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)

        dates = []
        current = start
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=step_days)

        return dates

    def get_month_info(self, date):
        """
        获取月份信息

        参数:
            date (str or datetime): 日期

        返回:
            dict: 月份信息
        """
        dt = self.parse_date(date)
        year = dt.year
        month = dt.month

        # 获取该月的第一天和最后一天
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        return {
            'year': year,
            'month': month,
            'month_name': calendar.month_name[month],
            'first_day': first_day.strftime('%Y-%m-%d'),
            'last_day': last_day.strftime('%Y-%m-%d'),
            'total_days': calendar.monthrange(year, month)[1],
            'weekday_of_first': calendar.day_name[first_day.weekday()]
        }

    def get_week_number(self, date):
        """
        获取周数

        参数:
            date (str or datetime): 日期

        返回:
            dict: 周数信息
        """
        dt = self.parse_date(date)

        return {
            'iso_week': dt.isocalendar()[1],
            'iso_year': dt.isocalendar()[0],
            'weekday': dt.weekday() + 1,
            'weekday_name': calendar.day_name[dt.weekday()]
        }

    def is_leap_year(self, year):
        """
        判断是否为闰年

        参数:
            year (int): 年份

        返回:
            bool: 是否为闰年
        """
        return calendar.isleap(year)

    def get_quarter(self, date):
        """
        获取季度信息

        参数:
            date (str or datetime): 日期

        返回:
            dict: 季度信息
        """
        dt = self.parse_date(date)
        quarter = (dt.month - 1) // 3 + 1

        quarter_months = {
            1: (1, 2, 3),
            2: (4, 5, 6),
            3: (7, 8, 9),
            4: (10, 11, 12)
        }

        first_month = quarter_months[quarter][0]
        last_month = quarter_months[quarter][2]

        first_day = datetime(dt.year, first_month, 1)
        last_day = datetime(dt.year, last_month, calendar.monthrange(dt.year, last_month)[1])

        return {
            'quarter': quarter,
            'year': dt.year,
            'first_day': first_day.strftime('%Y-%m-%d'),
            'last_day': last_day.strftime('%Y-%m-%d'),
            'formatted': f"Q{quarter} {dt.year}"
        }


# 示例使用
if __name__ == '__main__':
    calc = DateCalculator()

    # 示例1: 计算时间差
    diff = calc.time_difference('2024-01-01', '2024-02-25')
    print(f"Time difference: {diff}")

    # 示例2: 添加天数
    future = calc.add_days('2024-02-25', 30)
    print(f"\n30 days from now: {future}")

    # 示例3: 计算年龄
    age = calc.calculate_age('1990-05-15')
    print(f"\nAge: {age['formatted']}")

    # 示例4: 生成日期范围
    dates = calc.date_range('2024-02-25', '2024-03-05')
    print(f"\nDate range: {dates}")

    # 示例5: 获取月份信息
    month_info = calc.get_month_info('2024-02-25')
    print(f"\nMonth info: {month_info}")
