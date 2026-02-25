#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理器 - 提供常见的数据处理功能
"""

import json
import csv
import statistics
from datetime import datetime
from typing import List, Dict, Any, Optional


class DataProcessor:
    """数据处理类，提供多种数据处理功能"""
    
    def __init__(self):
        self.data = []
        self.stats = {}
    
    def load_json(self, filepath: str) -> List[Dict]:
        """从JSON文件加载数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"成功加载 {len(self.data)} 条数据")
            return self.data
        except Exception as e:
            print(f"加载JSON文件失败: {e}")
            return []
    
    def load_csv(self, filepath: str) -> List[Dict]:
        """从CSV文件加载数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            print(f"成功加载 {len(self.data)} 条数据")
            return self.data
        except Exception as e:
            print(f"加载CSV文件失败: {e}")
            return []
    
    def calculate_statistics(self, numeric_field: str) -> Dict[str, Any]:
        """计算数值字段的统计信息"""
        if not self.data:
            print("没有数据可分析")
            return {}
        
        try:
            values = [float(item[numeric_field]) for item in self.data if numeric_field in item]
            
            if not values:
                print(f"字段 '{numeric_field}' 没有数值数据")
                return {}
            
            self.stats = {
                'count': len(values),
                'sum': sum(values),
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'min': min(values),
                'max': max(values),
                'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                'variance': statistics.variance(values) if len(values) > 1 else 0,
                'field': numeric_field
            }
            
            return self.stats
        except Exception as e:
            print(f"计算统计信息失败: {e}")
            return {}
    
    def filter_data(self, condition_func) -> List[Dict]:
        """根据条件函数过滤数据"""
        return [item for item in self.data if condition_func(item)]
    
    def sort_data(self, key_field: str, reverse: bool = False) -> List[Dict]:
        """根据指定字段排序数据"""
        return sorted(self.data, key=lambda x: x.get(key_field, ''), reverse=reverse)
    
    def export_to_json(self, filepath: str, data: Optional[List[Dict]] = None) -> bool:
        """导出数据到JSON文件"""
        try:
            export_data = data if data is not None else self.data
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            print(f"数据已导出到 {filepath}")
            return True
        except Exception as e:
            print(f"导出JSON文件失败: {e}")
            return False
    
    def export_to_csv(self, filepath: str, data: Optional[List[Dict]] = None) -> bool:
        """导出数据到CSV文件"""
        try:
            export_data = data if data is not None else self.data
            if not export_data:
                print("没有数据可导出")
                return False
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
                writer.writeheader()
                writer.writerows(export_data)
            
            print(f"数据已导出到 {filepath}")
            return True
        except Exception as e:
            print(f"导出CSV文件失败: {e}")
            return False
    
    def print_summary(self):
        """打印数据摘要"""
        print("=" * 50)
        print("数据摘要")
        print("=" * 50)
        print(f"数据条数: {len(self.data)}")
        
        if self.data:
            print(f"字段: {list(self.data[0].keys())}")
        
        if self.stats:
            print("\n统计信息:")
            for key, value in self.stats.items():
                print(f"  {key}: {value}")
        
        print("=" * 50)


def generate_sample_data() -> List[Dict]:
    """生成示例数据"""
    return [
        {"id": 1, "name": "张三", "age": 25, "score": 85.5, "department": "技术部"},
        {"id": 2, "name": "李四", "age": 30, "score": 92.0, "department": "市场部"},
        {"id": 3, "name": "王五", "age": 28, "score": 78.5, "department": "技术部"},
        {"id": 4, "name": "赵六", "age": 35, "score": 88.0, "department": "人事部"},
        {"id": 5, "name": "钱七", "age": 22, "score": 95.5, "department": "市场部"},
    ]


def main():
    """主函数 - 演示数据处理器功能"""
    print("数据处理器演示")
    print("=" * 50)
    
    # 创建处理器实例
    processor = DataProcessor()
    
    # 使用示例数据
    sample_data = generate_sample_data()
    processor.data = sample_data
    
    # 打印数据摘要
    processor.print_summary()
    
    # 计算统计信息
    print("\n计算分数统计信息:")
    stats = processor.calculate_statistics("score")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 过滤数据
    print("\n过滤技术部员工:")
    tech_employees = processor.filter_data(lambda x: x.get("department") == "技术部")
    for emp in tech_employees:
        print(f"  {emp['name']} - {emp['score']}分")
    
    # 排序数据
    print("\n按分数降序排序:")
    sorted_data = processor.sort_data("score", reverse=True)
    for emp in sorted_data:
        print(f"  {emp['name']}: {emp['score']}分")
    
    # 导出数据
    processor.export_to_json("sample_data.json")
    processor.export_to_csv("sample_data.csv")
    
    print("\n演示完成！")


if __name__ == "__main__":
    main()