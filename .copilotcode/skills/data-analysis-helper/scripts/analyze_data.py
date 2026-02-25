#!/usr/bin/env python3
"""
数据分析辅助脚本
支持快速分析CSV/JSON文件并生成统计报告
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path


def analyze_csv(filepath):
    """分析CSV文件"""
    df = pd.read_csv(filepath)
    return generate_report(df, filepath)


def analyze_json(filepath):
    """分析JSON文件"""
    df = pd.read_json(filepath)
    return generate_report(df, filepath)


def generate_report(df, filepath):
    """生成数据分析报告"""
    report = {
        "file": filepath,
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
        "duplicates": df.duplicated().sum(),
        "numeric_summary": {}
    }
    
    # 数值列统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        report["numeric_summary"][col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "q25": float(df[col].quantile(0.25)),
            "q75": float(df[col].quantile(0.75))
        }
    
    # 分类列统计
    categorical_cols = df.select_dtypes(include=['object']).columns
    report["categorical_summary"] = {}
    for col in categorical_cols:
        value_counts = df[col].value_counts().head(10).to_dict()
        report["categorical_summary"][col] = {
            "unique_count": df[col].nunique(),
            "top_values": value_counts
        }
    
    return report


def print_report(report):
    """打印分析报告"""
    print("=" * 60)
    print(f"数据分析报告: {report['file']}")
    print("=" * 60)
    
    print(f"\n数据形状: {report['shape'][0]} 行 × {report['shape'][1]} 列")
    
    print("\n列信息:")
    for col, dtype in report['dtypes'].items():
        missing = report['missing_values'][col]
        missing_pct = report['missing_percentage'][col]
        print(f"  - {col}: {dtype} (缺失: {missing}, {missing_pct:.1f}%)")
    
    print(f"\n重复行数: {report['duplicates']}")
    
    if report['numeric_summary']:
        print("\n数值列统计:")
        for col, stats in report['numeric_summary'].items():
            print(f"\n  {col}:")
            print(f"    平均值: {stats['mean']:.2f}")
            print(f"    中位数: {stats['median']:.2f}")
            print(f"    标准差: {stats['std']:.2f}")
            print(f"    范围: [{stats['min']:.2f}, {stats['max']:.2f}]")
    
    if report['categorical_summary']:
        print("\n分类列统计:")
        for col, stats in report['categorical_summary'].items():
            print(f"\n  {col}:")
            print(f"    唯一值数量: {stats['unique_count']}")
            print(f"    最常见值:")
            for val, count in list(stats['top_values'].items())[:5]:
                print(f"      - {val}: {count}")
    
    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_data.py <文件路径>")
        print("支持格式: .csv, .json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    path = Path(filepath)
    
    if not path.exists():
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)
    
    try:
        if path.suffix.lower() == '.csv':
            report = analyze_csv(filepath)
        elif path.suffix.lower() == '.json':
            report = analyze_json(filepath)
        else:
            print(f"错误: 不支持的文件格式 - {path.suffix}")
            sys.exit(1)
        
        print_report(report)
        
        # 可选：保存JSON报告
        if len(sys.argv) > 2 and sys.argv[2] == '--save':
            output_path = path.stem + '_report.json'
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n报告已保存: {output_path}")
    
    except Exception as e:
        print(f"分析失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
