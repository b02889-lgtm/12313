#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用Python代码示例
包含常用的工具函数和示例
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


def greet(name: str) -> str:
    """简单的问候函数"""
    return f"你好，{name}！欢迎使用这个代码示例。"


def calculate_average(numbers: List[float]) -> float:
    """计算数字列表的平均值"""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def read_json_file(file_path: str) -> Dict[str, Any]:
    """读取JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在")
        return {}
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的JSON格式")
        return {}


def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """写入JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"写入文件时出错: {e}")
        return False


def get_current_time() -> str:
    """获取当前时间字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def process_text(text: str) -> Dict[str, Any]:
    """处理文本，返回统计信息"""
    return {
        "length": len(text),
        "word_count": len(text.split()),
        "line_count": len(text.split('\n')),
        "uppercase_count": sum(1 for c in text if c.isupper()),
        "lowercase_count": sum(1 for c in text if c.islower()),
        "digit_count": sum(1 for c in text if c.isdigit())
    }


def main():
    """主函数 - 演示各个功能"""
    print("=" * 50)
    print("Python代码示例")
    print("=" * 50)
    
    # 问候
    print(greet("用户"))
    print()
    
    # 计算平均值
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    avg = calculate_average(numbers)
    print(f"数字列表 {numbers} 的平均值是: {avg}")
    print()
    
    # 获取当前时间
    print(f"当前时间: {get_current_time()}")
    print()
    
    # 文本处理示例
    sample_text = "Hello World! 这是一个Python代码示例。"
    text_stats = process_text(sample_text)
    print("文本统计信息:")
    for key, value in text_stats.items():
        print(f"  {key}: {value}")
    print()
    
    # JSON文件操作示例
    sample_data = {
        "name": "示例数据",
        "version": "1.0",
        "created_at": get_current_time(),
        "items": ["项目1", "项目2", "项目3"]
    }
    
    json_file = "example_data.json"
    if write_json_file(json_file, sample_data):
        print(f"已创建JSON文件: {json_file}")
        
        # 读取并显示
        loaded_data = read_json_file(json_file)
        print("读取的数据:")
        print(json.dumps(loaded_data, ensure_ascii=False, indent=2))
    
    print()
    print("=" * 50)
    print("代码示例执行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
