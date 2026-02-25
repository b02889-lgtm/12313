#!/usr/bin/env python3
"""
代码优化助手示例脚本
提供代码分析和优化建议
"""

import time
from typing import Callable, Any


class CodeOptimizer:
    """代码优化工具类"""
    
    @staticmethod
    def measure_time(func: Callable) -> Callable:
        """性能测试装饰器"""
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"函数 {func.__name__} 执行时间: {(end - start) * 1000:.2f}ms")
            return result
        return wrapper
    
    @staticmethod
    def suggest_optimizations(code_snippet: str) -> list:
        """提供代码优化建议"""
        suggestions = []
        
        # 检测常见优化点
        if "for" in code_snippet and "append" in code_snippet:
            suggestions.append("考虑使用列表推导式替代循环append")
        
        if "==" in code_snippet and "None" in code_snippet:
            suggestions.append("使用 'is None' 替代 '== None' 进行None比较")
        
        if "while True" in code_snippet:
            suggestions.append("检查while True循环是否有明确的退出条件")
        
        if len(code_snippet.split('\n')) > 50:
            suggestions.append("建议将长函数拆分为多个小函数，遵循单一职责原则")
        
        return suggestions
    
    @staticmethod
    def format_code(code: str) -> str:
        """简单的代码格式化"""
        lines = code.split('\n')
        formatted = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('}', ']', ')')):
                indent_level = max(0, indent_level - 1)
            
            formatted.append('    ' * indent_level + stripped)
            
            if stripped.endswith(('{', '[', '(')):
                indent_level += 1
        
        return '\n'.join(formatted)


# 示例使用
if __name__ == "__main__":
    optimizer = CodeOptimizer()
    
    # 示例代码
    sample_code = """
def process_data(data):
    result = []
    for item in data:
        if item is not None:
            result.append(item * 2)
    return result
"""
    
    print("=== 代码优化助手 ===")
    print("\n原始代码:")
    print(sample_code)
    
    print("\n优化建议:")
    suggestions = optimizer.suggest_optimizations(sample_code)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n优化后的代码:")
    optimized = "[item * 2 for item in data if item is not None]"
    print(optimized)
