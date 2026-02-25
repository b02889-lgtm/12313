#!/usr/bin/env python3
"""
数据分析演示 - 使用纯Python分析 sample_data.csv
"""

import csv
import json
from collections import defaultdict
from statistics import mean, median, stdev


def load_csv(filepath):
    """加载CSV文件"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数值类型
            processed_row = {}
            for key, value in row.items():
                try:
                    processed_row[key] = int(value)
                except ValueError:
                    try:
                        processed_row[key] = float(value)
                    except ValueError:
                        processed_row[key] = value
            data.append(processed_row)
    return data


def analyze_data(data):
    """分析数据"""
    if not data:
        return {}
    
    # 获取列名
    columns = list(data[0].keys())
    
    # 分析结果
    report = {
        "总行数": len(data),
        "列名": columns,
        "数值列统计": {},
        "分类列统计": {}
    }
    
    for col in columns:
        values = [row[col] for row in data]
        
        # 检查是否为数值列
        if all(isinstance(v, (int, float)) for v in values):
            report["数值列统计"][col] = {
                "平均值": round(mean(values), 2),
                "中位数": round(median(values), 2),
                "最小值": min(values),
                "最大值": max(values),
                "总和": sum(values)
            }
            # 计算标准差（需要至少2个数据点）
            if len(values) >= 2:
                report["数值列统计"][col]["标准差"] = round(stdev(values), 2)
        
        # 分类列统计
        elif all(isinstance(v, str) for v in values):
            value_counts = defaultdict(int)
            for v in values:
                value_counts[v] += 1
            report["分类列统计"][col] = {
                "唯一值数量": len(value_counts),
                "最常见值": dict(sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5])
            }
    
    return report


def group_by(data, group_col, agg_col):
    """按列分组统计"""
    groups = defaultdict(list)
    for row in data:
        groups[row[group_col]].append(row[agg_col])
    
    result = {}
    for group, values in groups.items():
        result[group] = {
            "数量": len(values),
            "平均值": round(mean(values), 2),
            "总和": sum(values)
        }
    return result


def filter_data(data, condition):
    """筛选数据"""
    return [row for row in data if condition(row)]


def print_report(report):
    """打印分析报告"""
    print("=" * 60)
    print("           数据分析报告")
    print("=" * 60)
    
    print(f"\n>> 数据概览:")
    print(f"   总行数: {report['总行数']}")
    print(f"   列名: {', '.join(report['列名'])}")
    
    if report['数值列统计']:
        print(f"\n>> 数值列统计:")
        for col, stats in report['数值列统计'].items():
            print(f"\n   【{col}】")
            for key, value in stats.items():
                print(f"      {key}: {value}")
    
    if report['分类列统计']:
        print(f"\n>> 分类列统计:")
        for col, stats in report['分类列统计'].items():
            print(f"\n   【{col}】")
            print(f"      唯一值数量: {stats['唯一值数量']}")
            print(f"      最常见值:")
            for val, count in stats['最常见值'].items():
                print(f"         - {val}: {count}次")
    
    print("\n" + "=" * 60)


def main():
    # 加载数据
    print("正在加载数据...")
    data = load_csv('sample_data.csv')
    
    # 基本分析
    print("\n[1] 基本数据分析")
    report = analyze_data(data)
    print_report(report)
    
    # 分组统计示例
    print("\n[2] 按部门分组统计年龄")
    dept_age = group_by(data, 'department', 'age')
    print("   部门年龄统计:")
    for dept, stats in dept_age.items():
        print(f"      {dept}: 人数={stats['数量']}, 平均年龄={stats['平均值']}, 总年龄={stats['总和']}")
    
    print("\n[3] 按部门分组统计分数")
    dept_score = group_by(data, 'department', 'score')
    print("   部门分数统计:")
    for dept, stats in dept_score.items():
        print(f"      {dept}: 人数={stats['数量']}, 平均分={stats['平均值']}, 总分={stats['总和']}")
    
    # 筛选示例
    print("\n[4] 筛选年龄大于25岁的员工")
    older_employees = filter_data(data, lambda x: x['age'] > 25)
    print(f"   符合条件的员工 ({len(older_employees)}人):")
    for emp in older_employees:
        print(f"      - {emp['name']}: {emp['age']}岁, {emp['department']}, 分数{emp['score']}")
    
    # 筛选示例2
    print("\n[5] 筛选分数大于85分的员工")
    high_score_employees = filter_data(data, lambda x: x['score'] > 85)
    print(f"   符合条件的员工 ({len(high_score_employees)}人):")
    for emp in high_score_employees:
        print(f"      - {emp['name']}: {emp['score']}分")
    
    print("\n" + "=" * 60)
    print("数据分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
