#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 sample_data.csv 并生成报告
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

def analyze_sample_data():
    """分析示例数据并生成报告"""
    print("="*60)
    print("数据分析报告 - sample_data.csv")
    print("="*60)
    
    # 读取数据
    df = pd.read_csv('sample_data.csv', encoding='utf-8')
    print(f"✓ 成功加载数据: sample_data.csv")
    print(f"  数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
    
    # 创建报告字典
    report = {
        "报告生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "数据基本信息": {
            "文件名": "sample_data.csv",
            "行数": int(df.shape[0]),
            "列数": int(df.shape[1]),
            "列名": list(df.columns)
        },
        "数据类型": {},
        "数值统计": {},
        "分类统计": {},
        "数据质量": {}
    }
    
    # 数据类型
    for col, dtype in df.dtypes.items():
        report["数据类型"][col] = str(dtype)
    
    # 数值型数据统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            report["数值统计"][col] = {
                "计数": int(df[col].count()),
                "平均值": float(df[col].mean()),
                "标准差": float(df[col].std()),
                "最小值": float(df[col].min()),
                "最大值": float(df[col].max()),
                "中位数": float(df[col].median())
            }
    
    # 分类数据统计
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            report["分类统计"][col] = {
                "唯一值数量": int(value_counts.count()),
                "前3个值分布": {str(k): int(v) for k, v in value_counts.head(3).items()}
            }
    
    # 数据质量检查
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    report["数据质量"]["缺失值"] = {col: int(count) for col, count in missing.items() if count > 0}
    report["数据质量"]["总行数"] = int(len(df))
    report["数据质量"]["完整行数"] = int(len(df.dropna()))
    
    # 部门统计
    if 'department' in df.columns:
        dept_stats = df['department'].value_counts()
        report["部门统计"] = {str(dept): int(count) for dept, count in dept_stats.items()}
    
    # 年龄和分数分析
    if 'age' in df.columns and 'score' in df.columns:
        report["年龄分数分析"] = {
            "平均年龄": float(df['age'].mean()),
            "平均分数": float(df['score'].mean()),
            "年龄标准差": float(df['age'].std()),
            "分数标准差": float(df['score'].std()),
            "最高分": {
                "分数": float(df['score'].max()),
                "姓名": str(df.loc[df['score'].idxmax(), 'name']) if 'name' in df.columns else "未知"
            },
            "最低分": {
                "分数": float(df['score'].min()),
                "姓名": str(df.loc[df['score'].idxmin(), 'name']) if 'name' in df.columns else "未知"
            }
        }
    
    # 保存报告为JSON
    with open('data_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print("✓ 数据分析完成")
    print("✓ 报告已保存为: data_analysis_report.json")
    
    # 打印报告摘要
    print("\n" + "-"*60)
    print("报告摘要")
    print("-"*60)
    print(f"数据集大小: {report['数据基本信息']['行数']} 行 × {report['数据基本信息']['列数']} 列")
    print(f"列名: {', '.join(report['数据基本信息']['列名'])}")
    
    if '年龄分数分析' in report:
        print(f"平均年龄: {report['年龄分数分析']['平均年龄']:.1f} 岁")
        print(f"平均分数: {report['年龄分数分析']['平均分数']:.1f} 分")
        print(f"最高分: {report['年龄分数分析']['最高分']['分数']} 分 ({report['年龄分数分析']['最高分']['姓名']})")
        print(f"最低分: {report['年龄分数分析']['最低分']['分数']} 分 ({report['年龄分数分析']['最低分']['姓名']})")
    
    if '部门统计' in report:
        print("部门分布:")
        for dept, count in report['部门统计'].items():
            print(f"  {dept}: {count} 人")
    
    missing_total = sum(report['数据质量']['缺失值'].values())
    print(f"数据质量: 缺失值 {missing_total} 个")
    
    return report

if __name__ == "__main__":
    analyze_sample_data()