#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取当前时间的脚本（使用标准库）
"""

from datetime import datetime, timedelta

def get_current_time():
    """获取当前时间"""
    # 获取当前时间
    now = datetime.now()
    
    # 格式化输出
    print("*" * 50)
    print("⏰ 当前时间信息 ⏰")
    print("*" * 50)
    print(f"👉 完整时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"👉 ISO格式: {now.isoformat()}")
    print(f"👉 星期: {now.strftime('%A')} ({now.strftime('%w')})")
    print(f"👉 时间戳: {now.timestamp()}")
    print("*" * 50)
    
    return now

def get_weekday_chinese(weekday: int) -> str:
    """将weekday数字转换为中文星期名称"""
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return weekday_names[weekday]


def get_time_until_weekend():
    """计算距离周末还有多长时间"""
    now = datetime.now()
    
    # 获取当前是星期几（0=周一，6=周日）
    current_weekday = now.weekday()
    weekday_name = get_weekday_chinese(current_weekday)
    
    print(f"\n📅 今天是: {weekday_name}")
    
    # 计算距离周六（weekday=5）的时间
    if current_weekday < 5:  # 周一到周五
        days_until_saturday = 5 - current_weekday
        
        # 使用更精确的方式计算：直接算到下个周六的0点
        next_saturday = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_saturday)
        time_diff = next_saturday - now
        total_seconds = time_diff.total_seconds()
        
        # 转换为天时分秒
        days = int(total_seconds // (24 * 3600))
        hours = int((total_seconds % (24 * 3600)) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        print("\n⏳ 距离周末（周六）还有：")
        print(f"  📆 天数: {days}天")
        print(f"  🕐 小时: {hours}小时")
        print(f"  ⏱️  分钟: {minutes}分钟")
        print(f"  ⏲️  秒数: {seconds}秒")
        print(f"  📊 总分钟数: {total_seconds / 60:.2f}分钟")
        
        # 添加进度条
        total_workdays = 5
        passed_workdays = current_weekday
        progress = passed_workdays / total_workdays
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\n  📈 本周进度: [{bar}] {progress * 100:.0f}%")
    else:  # 周六或周日
        print("\n🎉 今天是周末！享受您的休息时间吧！🎉")

def get_greeting() -> str:
    """根据当前时间返回问候语"""
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return "🌅 早上好！新的一天开始了！"
    elif 9 <= hour < 12:
        return "☀️ 上午好！祝您工作顺利！"
    elif 12 <= hour < 14:
        return "🍽️ 中午好！记得吃午饭哦！"
    elif 14 <= hour < 18:
        return "🌤️ 下午好！继续加油！"
    elif 18 <= hour < 22:
        return "🌙 晚上好！辛苦了一天！"
    else:
        return "🌃 夜深了！注意休息哦！"


if __name__ == "__main__":
    # 显示问候语
    print(get_greeting())
    print()
    
    # 获取当前时间
    current_time = get_current_time()
    
    # 计算距离周末的时间
    get_time_until_weekend()
    
    print("\n" + "*" * 50)
    print("感谢使用时间工具！再见！👋")
    print("*" * 50)