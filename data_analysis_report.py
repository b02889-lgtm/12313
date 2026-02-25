# -*- coding: utf-8 -*-
"""
数据分析报告
使用数据分析助手技能生成
"""

import pandas as pd
import json

# 1. 加载数据
print("=" * 60)
print("1. 数据加载")
print("=" * 60)

# 加载CSV
df_csv = pd.read_csv('sample_data.csv')
print("\nCSV数据预览：")
print(df_csv)

# 加载JSON
with open('sample_data.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)
df_json = pd.DataFrame(data_json)
print("\nJSON数据预览：")
print(df_json)

# 2. 数据探索
print("\n" + "=" * 60)
print("2. 数据探索")
print("=" * 60)

print("\n数据类型信息：")
print(df_csv.dtypes)

print("\n基本统计信息：")
print(df_csv.describe())

print("\n部门分布：")
print(df_csv['department'].value_counts())

# 3. 数据分析
print("\n" + "=" * 60)
print("3. 数据分析")
print("=" * 60)

print("\n平均年龄：", df_csv['age'].mean())
print("平均分数：", df_csv['score'].mean())
print("年龄标准差：", df_csv['age'].std())
print("分数标准差：", df_csv['score'].std())

print("\n按部门分组统计：")
dept_stats = df_csv.groupby('department').agg({
    'age': ['mean', 'min', 'max'],
    'score': ['mean', 'min', 'max']
})
print(dept_stats)

print("\n分数最高的人员：")
max_score_idx = df_csv['score'].idxmax()
print(df_csv.loc[max_score_idx])

# 4. 数据筛选
print("\n" + "=" * 60)
print("4. 数据筛选")
print("=" * 60)

print("\n分数大于90的人员：")
high_scorers = df_csv[df_csv['score'] > 90]
print(high_scorers)

print("\n技术部人员：")
tech_dept = df_csv[df_csv['department'] == '技术部']
print(tech_dept)

# 5. 相关性分析
print("\n" + "=" * 60)
print("5. 相关性分析")
print("=" * 60)

print("\n年龄与分数的相关性：")
correlation = df_csv['age'].corr(df_csv['score'])
print(f"相关系数: {correlation:.4f}")

print("\n" + "=" * 60)
print("分析完成！")
print("=" * 60)
