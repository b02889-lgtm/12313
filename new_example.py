#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一个简单的 Python 示例脚本
演示基本的编程概念
"""

import random
from datetime import datetime


class Person:
    """人员类"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        """打招呼"""
        return f"你好，我是 {self.name}，今年 {self.age} 岁"
    
    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"


def generate_random_numbers(count, min_val, max_val):
    """生成随机数列表"""
    return [random.randint(min_val, max_val) for _ in range(count)]


def calculate_average(numbers):
    """计算平均值"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def main():
    """主函数"""
    print("=" * 50)
    print("Python 示例程序")
    print("=" * 50)
    
    # 创建人员对象
    person1 = Person("张三", 25)
    person2 = Person("李四", 30)
    
    print(f"\n{person1.greet()}")
    print(f"{person2.greet()}")
    
    # 生成随机数并计算平均值
    numbers = generate_random_numbers(10, 1, 100)
    print(f"\n生成的随机数: {numbers}")
    print(f"平均值: {calculate_average(numbers):.2f}")
    
    # 显示当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n当前时间: {current_time}")
    
    print("\n" + "=" * 50)
    print("程序执行完毕！")
    print("=" * 50)


if __name__ == "__main__":
    main()
