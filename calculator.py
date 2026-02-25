"""
高级计算器程序
支持复杂表达式计算、多数字运算、数学函数等
"""

import math
import re
from typing import List, Union, Optional
from collections import deque


class Calculator:
    """高级计算器类"""
    
    def __init__(self):
        """初始化计算器"""
        self.history = []  # 计算历史
        self.variables = {}  # 变量存储
        self.max_history = 50  # 最大历史记录数
    
    # ==================== 基础运算 ====================
    
    def add(self, *args) -> float:
        """加法 - 支持多个数字"""
        return sum(args)
    
    def subtract(self, a: float, *args) -> float:
        """减法 - 支持多个数字（从左到右依次减）"""
        result = a
        for num in args:
            result -= num
        return result
    
    def multiply(self, *args) -> float:
        """乘法 - 支持多个数字"""
        result = 1
        for num in args:
            result *= num
        return result
    
    def divide(self, a: float, *args) -> float:
        """除法 - 支持多个数字（从左到右依次除）"""
        result = a
        for num in args:
            if num == 0:
                raise ValueError("除数不能为零")
            result /= num
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """幂运算"""
        return base ** exponent
    
    def modulo(self, a: float, b: float) -> float:
        """取模运算"""
        if b == 0:
            raise ValueError("除数不能为零")
        return a % b
    
    def absolute(self, x: float) -> float:
        """绝对值"""
        return abs(x)
    
    # ==================== 高级数学函数 ====================
    
    def sqrt(self, x: float) -> float:
        """平方根"""
        if x < 0:
            raise ValueError("不能对负数求平方根")
        return math.sqrt(x)
    
    def cbrt(self, x: float) -> float:
        """立方根"""
        return x ** (1/3) if x >= 0 else -((-x) ** (1/3))
    
    def log(self, x: float, base: float = math.e) -> float:
        """对数运算 - 默认自然对数"""
        if x <= 0:
            raise ValueError("对数的真数必须大于零")
        if base <= 0 or base == 1:
            raise ValueError("对数的底数必须大于零且不等于1")
        return math.log(x, base)
    
    def ln(self, x: float) -> float:
        """自然对数"""
        if x <= 0:
            raise ValueError("对数的真数必须大于零")
        return math.log(x)
    
    def log10(self, x: float) -> float:
        """常用对数（以10为底）"""
        if x <= 0:
            raise ValueError("对数的真数必须大于零")
        return math.log10(x)
    
    def factorial(self, n: int) -> int:
        """阶乘"""
        if not isinstance(n, int):
            raise ValueError("阶乘只支持整数")
        if n < 0:
            raise ValueError("阶乘不支持负数")
        if n > 170:
            raise ValueError("数字太大，无法计算阶乘")
        return math.factorial(n)
    
    # ==================== 三角函数 ====================
    
    def sin(self, x: float, degree: bool = False) -> float:
        """正弦函数 - degree=True表示输入为度"""
        if degree:
            x = math.radians(x)
        return math.sin(x)
    
    def cos(self, x: float, degree: bool = False) -> float:
        """余弦函数 - degree=True表示输入为度"""
        if degree:
            x = math.radians(x)
        return math.cos(x)
    
    def tan(self, x: float, degree: bool = False) -> float:
        """正切函数 - degree=True表示输入为度"""
        if degree:
            x = math.radians(x)
        return math.tan(x)
    
    def asin(self, x: float, degree: bool = False) -> float:
        """反正弦函数"""
        if x < -1 or x > 1:
            raise ValueError("反正弦函数的输入必须在[-1, 1]范围内")
        result = math.asin(x)
        return math.degrees(result) if degree else result
    
    def acos(self, x: float, degree: bool = False) -> float:
        """反余弦函数"""
        if x < -1 or x > 1:
            raise ValueError("反余弦函数的输入必须在[-1, 1]范围内")
        result = math.acos(x)
        return math.degrees(result) if degree else result
    
    def atan(self, x: float, degree: bool = False) -> float:
        """反正切函数"""
        result = math.atan(x)
        return math.degrees(result) if degree else result
    
    # ==================== 统计函数 ====================
    
    def sum_values(self, *args) -> float:
        """求和"""
        return sum(args)
    
    def average(self, *args) -> float:
        """平均值"""
        if not args:
            raise ValueError("至少需要输入一个数字")
        return sum(args) / len(args)
    
    def max_value(self, *args) -> float:
        """最大值"""
        if not args:
            raise ValueError("至少需要输入一个数字")
        return max(args)
    
    def min_value(self, *args) -> float:
        """最小值"""
        if not args:
            raise ValueError("至少需要输入一个数字")
        return min(args)
    
    def std_dev(self, *args) -> float:
        """标准差"""
        if len(args) < 2:
            raise ValueError("计算标准差至少需要两个数字")
        mean = sum(args) / len(args)
        variance = sum((x - mean) ** 2 for x in args) / len(args)
        return math.sqrt(variance)
    
    # ==================== 进制转换 ====================
    
    def to_binary(self, n: int) -> str:
        """转换为二进制"""
        return bin(int(n))[2:]
    
    def to_octal(self, n: int) -> str:
        """转换为八进制"""
        return oct(int(n))[2:]
    
    def to_hex(self, n: int) -> str:
        """转换为十六进制"""
        return hex(int(n))[2:].upper()
    
    def from_binary(self, s: str) -> int:
        """从二进制转换"""
        return int(s, 2)
    
    def from_octal(self, s: str) -> int:
        """从八进制转换"""
        return int(s, 8)
    
    def from_hex(self, s: str) -> int:
        """从十六进制转换"""
        return int(s, 16)
    
    # ==================== 表达式解析 ====================
    
    def evaluate(self, expression: str) -> float:
        """
        解析并计算数学表达式
        支持: +, -, *, /, **, %, (), 以及数学函数
        """
        try:
            # 替换变量
            for var_name, var_value in self.variables.items():
                expression = expression.replace(var_name, str(var_value))
            
            # 安全地计算表达式
            result = self._safe_eval(expression)
            
            # 记录历史
            self._add_to_history(expression, result)
            
            return result
        except Exception as e:
            raise ValueError(f"表达式计算错误: {e}")
    
    def _safe_eval(self, expression: str) -> float:
        """安全地计算表达式"""
        # 清理表达式
        expression = expression.replace(' ', '')
        
        # 允许的字符和函数
        allowed_chars = set('0123456789+-*/.()%,')
        allowed_functions = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                            'sqrt', 'cbrt', 'log', 'ln', 'log10', 'abs',
                            'pi', 'e', 'fact', 'factorial']
        
        # 替换数学常数
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
        
        # 使用更安全的方式解析
        try:
            # 先尝试直接计算简单表达式
            result = eval(expression, {"__builtins__": {}}, {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
                'abs': abs, 'pow': pow, 'factorial': math.factorial
            })
            return result
        except:
            raise ValueError("无效的表达式")
    
    # ==================== 变量和历史管理 ====================
    
    def set_variable(self, name: str, value: float):
        """设置变量"""
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            raise ValueError("变量名必须以字母或下划线开头，只能包含字母、数字和下划线")
        self.variables[name] = value
    
    def get_variable(self, name: str) -> float:
        """获取变量值"""
        if name not in self.variables:
            raise ValueError(f"变量 '{name}' 不存在")
        return self.variables[name]
    
    def delete_variable(self, name: str):
        """删除变量"""
        if name in self.variables:
            del self.variables[name]
    
    def list_variables(self) -> dict:
        """列出所有变量"""
        return self.variables.copy()
    
    def clear_variables(self):
        """清除所有变量"""
        self.variables.clear()
    
    def _add_to_history(self, expression: str, result: float):
        """添加计算历史"""
        self.history.append({"expression": expression, "result": result})
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_history(self, n: Optional[int] = None) -> List[dict]:
        """获取计算历史"""
        if n is None:
            return self.history.copy()
        return self.history[-n:].copy()
    
    def clear_history(self):
        """清除历史"""
        self.history.clear()
    
    def show_history(self, n: int = 10):
        """显示计算历史"""
        if not self.history:
            print("暂无计算历史")
            return
        
        print("\n" + "=" * 50)
        print("计算历史")
        print("=" * 50)
        for i, item in enumerate(self.history[-n:], 1):
            print(f"{i}. {item['expression']} = {item['result']}")
        print("=" * 50)


def print_menu():
    """打印主菜单"""
    print("\n" + "=" * 60)
    print("           高级计算器 - 支持复杂计算")
    print("=" * 60)
    print("【基础运算】")
    print("  1. 加法 (+)          2. 减法 (-)")
    print("  3. 乘法 (*)          4. 除 (/)")
    print("  5. 幂运算 (**)       6. 取模 (%)")
    print("\n【数学函数】")
    print("  7. 平方根 (sqrt)     8. 立方根 (cbrt)")
    print("  9. 对数 (log)       10. 自然对数 (ln)")
    print(" 11. 阶乘 (!)         12. 绝对值 (abs)")
    print("\n【三角函数】")
    print(" 13. 正弦 (sin)       14. 余弦 (cos)")
    print(" 15. 正切 (tan)")
    print("\n【统计函数】")
    print(" 16. 平均值 (avg)     17. 最大值 (max)")
    print(" 18. 最小值 (min)     19. 标准差 (std)")
    print("\n【高级功能】")
    print(" 20. 表达式计算       21. 设置变量")
    print(" 22. 查看变量         23. 计算历史")
    print(" 24. 进制转换")
    print("\n  0. 退出")
    print("=" * 60)


def get_numbers(prompt: str, count: int = 2) -> List[float]:
    """获取多个数字输入"""
    numbers = []
    print(f"\n{prompt} (用空格分隔)")
    user_input = input("> ").strip()
    try:
        numbers = [float(x) for x in user_input.split()]
        if len(numbers) < count:
            raise ValueError(f"至少需要输入 {count} 个数字")
        return numbers
    except ValueError as e:
        raise ValueError(f"输入格式错误: {e}")


def main():
    """主函数"""
    calc = Calculator()
    
    print("\n欢迎使用高级计算器！")
    print("支持复杂表达式、多数字运算、数学函数等")
    
    while True:
        print_menu()
        choice = input("\n请选择操作 (0-24): ").strip()
        
        try:
            if choice == '0':
                print("\n感谢使用，再见！")
                break
            
            # 基础运算
            elif choice == '1':
                nums = get_numbers("请输入要相加的数字", 2)
                result = calc.add(*nums)
                print(f"\n结果: {' + '.join(map(str, nums))} = {result}")
            
            elif choice == '2':
                nums = get_numbers("请输入要相减的数字", 2)
                result = calc.subtract(*nums)
                print(f"\n结果: {' - '.join(map(str, nums))} = {result}")
            
            elif choice == '3':
                nums = get_numbers("请输入要相乘的数字", 2)
                result = calc.multiply(*nums)
                print(f"\n结果: {' × '.join(map(str, nums))} = {result}")
            
            elif choice == '4':
                nums = get_numbers("请输入要相除的数字", 2)
                result = calc.divide(*nums)
                print(f"\n结果: {' ÷ '.join(map(str, nums))} = {result}")
            
            elif choice == '5':
                base = float(input("请输入底数: "))
                exp = float(input("请输入指数: "))
                result = calc.power(base, exp)
                print(f"\n结果: {base} ** {exp} = {result}")
            
            elif choice == '6':
                a = float(input("请输入被除数: "))
                b = float(input("请输入除数: "))
                result = calc.modulo(a, b)
                print(f"\n结果: {a} % {b} = {result}")
            
            # 数学函数
            elif choice == '7':
                x = float(input("请输入数字: "))
                result = calc.sqrt(x)
                print(f"\n结果: √{x} = {result}")
            
            elif choice == '8':
                x = float(input("请输入数字: "))
                result = calc.cbrt(x)
                print(f"\n结果: ³√{x} = {result}")
            
            elif choice == '9':
                x = float(input("请输入真数: "))
                base_input = input("请输入底数 (默认e): ").strip()
                base = float(base_input) if base_input else math.e
                result = calc.log(x, base)
                print(f"\n结果: log_{base}({x}) = {result}")
            
            elif choice == '10':
                x = float(input("请输入数字: "))
                result = calc.ln(x)
                print(f"\n结果: ln({x}) = {result}")
            
            elif choice == '11':
                n = int(input("请输入非负整数: "))
                result = calc.factorial(n)
                print(f"\n结果: {n}! = {result}")
            
            elif choice == '12':
                x = float(input("请输入数字: "))
                result = calc.absolute(x)
                print(f"\n结果: |{x}| = {result}")
            
            # 三角函数
            elif choice == '13':
                x = float(input("请输入角度/弧度: "))
                is_degree = input("是否使用角度制? (y/n, 默认n): ").strip().lower() == 'y'
                result = calc.sin(x, is_degree)
                unit = "度" if is_degree else "弧度"
                print(f"\n结果: sin({x}{unit}) = {result}")
            
            elif choice == '14':
                x = float(input("请输入角度/弧度: "))
                is_degree = input("是否使用角度制? (y/n, 默认n): ").strip().lower() == 'y'
                result = calc.cos(x, is_degree)
                unit = "度" if is_degree else "弧度"
                print(f"\n结果: cos({x}{unit}) = {result}")
            
            elif choice == '15':
                x = float(input("请输入角度/弧度: "))
                is_degree = input("是否使用角度制? (y/n, 默认n): ").strip().lower() == 'y'
                result = calc.tan(x, is_degree)
                unit = "度" if is_degree else "弧度"
                print(f"\n结果: tan({x}{unit}) = {result}")
            
            # 统计函数
            elif choice == '16':
                nums = get_numbers("请输入数字", 1)
                result = calc.average(*nums)
                print(f"\n结果: 平均值 = {result}")
            
            elif choice == '17':
                nums = get_numbers("请输入数字", 1)
                result = calc.max_value(*nums)
                print(f"\n结果: 最大值 = {result}")
            
            elif choice == '18':
                nums = get_numbers("请输入数字", 1)
                result = calc.min_value(*nums)
                print(f"\n结果: 最小值 = {result}")
            
            elif choice == '19':
                nums = get_numbers("请输入数字", 2)
                result = calc.std_dev(*nums)
                print(f"\n结果: 标准差 = {result}")
            
            # 高级功能
            elif choice == '20':
                print("\n支持的操作符: +, -, *, /, **, %, ()")
                print("支持的函数: sin, cos, tan, sqrt, log, ln, abs")
                print("支持的常数: pi, e")
                print("示例: (1+2)*3, sin(pi/2), sqrt(16)+5")
                expr = input("\n请输入表达式: ").strip()
                result = calc.evaluate(expr)
                print(f"\n结果: {expr} = {result}")
            
            elif choice == '21':
                name = input("请输入变量名: ").strip()
                value = float(input("请输入变量值: "))
                calc.set_variable(name, value)
                print(f"\n变量设置成功: {name} = {value}")
            
            elif choice == '22':
                vars_dict = calc.list_variables()
                if vars_dict:
                    print("\n已定义的变量:")
                    for name, value in vars_dict.items():
                        print(f"  {name} = {value}")
                else:
                    print("\n暂无变量定义")
            
            elif choice == '23':
                calc.show_history()
            
            elif choice == '24':
                print("\n进制转换:")
                print("  1. 十进制 → 二进制")
                print("  2. 十进制 → 八进制")
                print("  3. 十进制 → 十六进制")
                print("  4. 二进制 → 十进制")
                print("  5. 八进制 → 十进制")
                print("  6. 十六进制 → 十进制")
                conv_choice = input("\n请选择 (1-6): ").strip()
                
                if conv_choice == '1':
                    n = int(input("请输入十进制数: "))
                    print(f"\n结果: {n} = 0b{calc.to_binary(n)}")
                elif conv_choice == '2':
                    n = int(input("请输入十进制数: "))
                    print(f"\n结果: {n} = 0o{calc.to_octal(n)}")
                elif conv_choice == '3':
                    n = int(input("请输入十进制数: "))
                    print(f"\n结果: {n} = 0x{calc.to_hex(n)}")
                elif conv_choice == '4':
                    s = input("请输入二进制数: ").strip()
                    print(f"\n结果: 0b{s} = {calc.from_binary(s)}")
                elif conv_choice == '5':
                    s = input("请输入八进制数: ").strip()
                    print(f"\n结果: 0o{s} = {calc.from_octal(s)}")
                elif conv_choice == '6':
                    s = input("请输入十六进制数: ").strip()
                    print(f"\n结果: 0x{s} = {calc.from_hex(s)}")
            
            else:
                print("\n无效的选择，请重新输入！")
        
        except ValueError as e:
            print(f"\n错误: {e}")
        except Exception as e:
            print(f"\n发生错误: {e}")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
