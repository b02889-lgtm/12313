# -*- coding: utf-8 -*-
"""
高级数学计算示例
使用Calculator技能
"""

import math
import numpy as np


def solve_quadratic(a: float, b: float, c: float) -> tuple:
    """
    解二次方程 ax² + bx + c = 0

    Args:
        a: 二次项系数
        b: 一次项系数
        c: 常数项

    Returns:
        (x1, x2) 或 None（无实数解时）
    """
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return x1, x2
    else:
        return None  # 复数根


def numerical_derivative(f, x: float, h: float = 1e-5) -> float:
    """
    数值微分（中心差分法）

    Args:
        f: 函数
        x: 求导点
        h: 步长

    Returns:
        导数值
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def matrix_operations():
    """矩阵运算示例"""
    # 创建矩阵
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    print("矩阵A：")
    print(A)

    print("\n矩阵B：")
    print(B)

    print("\n矩阵乘法 A × B：")
    C = np.dot(A, B)
    print(C)

    print("\n矩阵A的逆：")
    A_inv = np.linalg.inv(A)
    print(A_inv)

    print("\n矩阵A的行列式：")
    det_A = np.linalg.det(A)
    print(f"det(A) = {det_A}")

    print("\n矩阵A的特征值和特征向量：")
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")


def solve_linear_system():
    """解线性方程组示例"""
    # 方程组：
    # 2x + 3y = 8
    # x - y = -1

    A = np.array([[2, 3], [1, -1]])
    b = np.array([8, -1])

    print("线性方程组：")
    print("2x + 3y = 8")
    print("x - y = -1")

    solution = np.linalg.solve(A, b)
    print(f"\n解：x = {solution[0]}, y = {solution[1]}")


def statistics_demo():
    """统计计算示例"""
    data = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41]

    print("\n统计数据：", data)
    print(f"平均值: {np.mean(data)}")
    print(f"中位数: {np.median(data)}")
    print(f"标准差: {np.std(data)}")
    print(f"方差: {np.var(data)}")
    print(f"最小值: {np.min(data)}")
    print(f"最大值: {np.max(data)}")


def main():
    """主函数"""
    print("=" * 60)
    print("高级数学计算示例")
    print("=" * 60)

    # 1. 解二次方程
    print("\n1. 解二次方程 x² - 5x + 6 = 0")
    roots = solve_quadratic(1, -5, 6)
    if roots:
        print(f"   解: x1 = {roots[0]}, x2 = {roots[1]}")

    # 2. 数值微分
    print("\n2. 数值微分示例 f(x) = x² 在 x=3 处")
    def f(x):
        return x**2
    derivative = numerical_derivative(f, 3)
    print(f"   f'(3) = {derivative} (理论值: 6)")

    # 3. 矩阵运算
    print("\n3. 矩阵运算")
    matrix_operations()

    # 4. 解线性方程组
    print("\n4. 解线性方程组")
    solve_linear_system()

    # 5. 统计计算
    print("\n5. 统计计算")
    statistics_demo()

    print("\n" + "=" * 60)
    print("计算完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
