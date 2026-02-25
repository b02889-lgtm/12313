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
    print("=" * 50)
    print("当前时间信息")
    print("=" * 50)
    print(f"完整时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"ISO格式: {now.isoformat()}")
    print(f"星期: {now.strftime('%A')} ({now.strftime('%w')})")
    print(f"时间戳: {now.timestamp()}")
    print("=" * 50)
    
    return now

def get_time_until_weekend():
    """计算距离周末还有多长时间"""
    now = datetime.now()
    
    # 获取当前是星期几（0=周一，6=周日）
    current_weekday = now.weekday()
    
    # 计算距离周六（weekday=5）的时间
    if current_weekday < 5:  # 周一到周五
        days_until_saturday = 5 - current_weekday
        
        # 计算到周六00:00:00的时间
        # 先计算到今天午夜的时间
        end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        time_until_midnight = end_of_today - now
        
        # 加上完整的天数
        total_seconds = time_until_midnight.total_seconds() + (days_until_saturday - 1) * 24 * 3600
        
        # 转换为天时分秒
        days = int(total_seconds // (24 * 3600))
        hours = int((total_seconds % (24 * 3600)) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        
        print("\n距离周末（周六）还有：")
        print(f"天数: {days}天")
        print(f"小时: {hours}小时")
        print(f"分钟: {minutes}分钟")
        print(f"秒数: {seconds}秒")
        print(f"总分钟数: {total_seconds / 60:.2f}分钟")
    else:  # 周六或周日
        print("\n今天是周末！享受您的休息时间吧！")

if __name__ == "__main__":
    # 获取当前时间
    current_time = get_current_time()
    
    # 计算距离周末的时间
    get_time_until_weekend()