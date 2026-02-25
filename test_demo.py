# -*- coding: utf-8 -*-
"""
Calculator 单元测试
"""

import unittest
from demo import Calculator


class TestCalculator(unittest.TestCase):
    """Calculator 测试类"""

    def setUp(self):
        """测试前初始化"""
        self.calc = Calculator()

    def test_add(self):
        """测试加法"""
        self.assertEqual(self.calc.add(1, 2), 3)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        """测试减法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
        self.assertEqual(self.calc.subtract(0, 0), 0)

    def test_multiply(self):
        """测试乘法"""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 5), 0)

    def test_divide(self):
        """测试除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)

    def test_divide_by_zero(self):
        """测试除以零错误"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_power(self):
        """测试幂运算"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(2, -1), 0.5)

    def test_modulo(self):
        """测试取余"""
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(7, 2), 1)
        self.assertEqual(self.calc.modulo(10, 5), 0)

    def test_modulo_by_zero(self):
        """测试取余除以零错误"""
        with self.assertRaises(ValueError):
            self.calc.modulo(10, 0)

    def test_history(self):
        """测试历史记录"""
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history)
        self.assertIn("5 - 3 = 2", history)


if __name__ == "__main__":
    unittest.main()
