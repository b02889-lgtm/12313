# -*- coding: utf-8 -*-
"""
示例项目文件
包含一些基本的Python代码示例
"""

import re


class ValidationError(Exception):
    """验证错误异常"""
    pass


class InputValidator:
    """输入验证器类"""
    
    @staticmethod
    def validate_number(value, name="数值"):
        """验证是否为有效数字"""
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{name}必须是数字类型")
        return float(value)
    
    @staticmethod
    def validate_non_zero(value, name="除数"):
        """验证不为零"""
        if value == 0:
            raise ValidationError(f"{name}不能为零")
        return value
    
    @staticmethod
    def validate_positive(value, name="数值"):
        """验证为正数"""
        if value <= 0:
            raise ValidationError(f"{name}必须是正数")
        return value


class Calculator:
    """简单的计算器类"""

    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        """加法运算"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        """除法运算"""
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, a: float, b: float) -> float:
        """幂运算（求a的b次方）"""
        result = a ** b
        self.history.append(f"{a} ** {b} = {result}")
        return result

    def modulo(self, a: float, b: float) -> float:
        """取余运算"""
        if b == 0:
            raise ValueError("除数不能为零")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        return result

    def get_history(self) -> list:
        """获取计算历史"""
        return self.history


def main():
    """主函数"""
    calc = Calculator()

    # 测试基本运算
    print("计算器测试：")
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"10 - 5 = {calc.subtract(10, 5)}")
    print(f"10 * 5 = {calc.multiply(10, 5)}")
    print(f"10 / 5 = {calc.divide(10, 5)}")

    # 测试新功能
    print("\n新功能测试：")
    print(f"2 ** 3 = {calc.power(2, 3)}")
    print(f"10 % 3 = {calc.modulo(10, 3)}")

    # 测试错误处理
    print("\n错误处理测试：")
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"  捕获错误: {e}")

    try:
        calc.modulo(10, 0)
    except ValueError as e:
        print(f"  捕获错误: {e}")

    # 打印历史记录
    print("\n计算历史：")
    for item in calc.get_history():
        print(f"  - {item}")


if __name__ == "__main__":
    main()
