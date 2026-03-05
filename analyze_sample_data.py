# -*- coding: utf-8 -*-
"""
数据分析脚本 - 基于 sample_data.csv
按照数据分析工作流执行完整分析
"""

import sys
import io
import pandas as pd
import numpy as np

# 修复 Windows 终端编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("         数据分析报告 - sample_data.csv")
print("=" * 60)

# ===== 步骤1：数据加载 =====
print("\n【步骤1】数据加载")
print("-" * 40)
df = pd.read_csv('sample_data.csv')
print(f"[OK] 数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")

# ===== 步骤2：数据探索 =====
print("\n【步骤2】数据探索")
print("-" * 40)

print("\n>>> 数据预览（前5行）：")
print(df.to_string(index=False))

print("\n>>> 数据结构信息：")
print(f"  列名：{list(df.columns)}")
for col in df.columns:
    print(f"  - {col}: 类型={df[col].dtype}, 非空={df[col].notna().sum()}/{len(df)}")

print("\n>>> 缺失值检查：")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("  [OK] 无缺失值")
else:
    print(f"  [!] 存在缺失值：\n{missing[missing > 0]}")

print("\n>>> 重复行检查：")
dup_count = df.duplicated().sum()
if dup_count == 0:
    print("  [OK] 无重复行")
else:
    print(f"  [!] 发现 {dup_count} 行重复数据")

# ===== 步骤3：数据清洗 =====
print("\n【步骤3】数据清洗")
print("-" * 40)
df_clean = df.copy()
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.dropna()
print(f"[OK] 清洗完成，剩余有效数据：{len(df_clean)} 行")

# ===== 步骤4：统计分析 =====
print("\n【步骤4】统计分析")
print("-" * 40)

# 数值列统计
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [c for c in numeric_cols if c != 'id']  # 排除id列

print(f"\n>>> 数值列（{numeric_cols}）统计摘要：")
stats = df_clean[numeric_cols].describe()
print(stats.to_string())

# age 分析
print(f"\n>>> 年龄分析：")
print(f"  平均年龄：{df_clean['age'].mean():.1f} 岁")
print(f"  最小年龄：{df_clean['age'].min()} 岁  最大年龄：{df_clean['age'].max()} 岁")
print(f"  年龄中位数：{df_clean['age'].median():.1f} 岁")
print(f"  年龄标准差：{df_clean['age'].std():.2f}")

# score 分析
print(f"\n>>> 成绩分析：")
print(f"  平均分：{df_clean['score'].mean():.2f}")
print(f"  最高分：{df_clean['score'].max()}  最低分：{df_clean['score'].min()}")
print(f"  中位数：{df_clean['score'].median():.2f}")
print(f"  标准差：{df_clean['score'].std():.2f}")

# 找出最高分和最低分
top = df_clean.loc[df_clean['score'].idxmax()]
bottom = df_clean.loc[df_clean['score'].idxmin()]
print(f"  最高分人员：{top['name']}（{top['score']}分，{top['department']}）")
print(f"  最低分人员：{bottom['name']}（{bottom['score']}分，{bottom['department']}）")

# 分组分析（按部门）
print(f"\n>>> 按部门分组统计：")
dept_stats = df_clean.groupby('department').agg(
    人数=('id', 'count'),
    平均年龄=('age', 'mean'),
    平均成绩=('score', 'mean'),
    最高成绩=('score', 'max'),
    最低成绩=('score', 'min')
).round(2)
print(dept_stats.to_string())

# 相关性分析
print(f"\n>>> 相关性分析（age vs score）：")
corr = df_clean[['age', 'score']].corr().loc['age', 'score']
print(f"  年龄与成绩的相关系数：{corr:.4f}")
if abs(corr) < 0.3:
    level = "弱相关"
elif abs(corr) < 0.7:
    level = "中等相关"
else:
    level = "强相关"
direction = "正" if corr > 0 else "负"
print(f"  结论：年龄与成绩呈{direction}{level}")

# ===== 步骤5：成绩分级 =====
print(f"\n【步骤5】成绩分级分析")
print("-" * 40)

def grade(score):
    if score >= 90:
        return 'A(优秀)'
    elif score >= 80:
        return 'B(良好)'
    elif score >= 70:
        return 'C(中等)'
    else:
        return 'D(待提升)'

df_clean = df_clean.copy()
df_clean['grade'] = df_clean['score'].apply(grade)
print("\n  姓名    成绩   等级       部门")
print("  " + "-" * 36)
for _, row in df_clean.iterrows():
    print(f"  {row['name']:4s}  {row['score']:5.1f}  {row['grade']:8s}  {row['department']}")

print(f"\n>>> 各等级人数统计：")
grade_counts = df_clean['grade'].value_counts().sort_index()
for g, cnt in grade_counts.items():
    print(f"  {g}：{cnt} 人")

# ===== 步骤6：可视化建议 =====
print(f"\n【步骤6】可视化建议")
print("-" * 40)
print("  建议图表类型：")
print("  1. 柱状图：各部门平均成绩对比")
print("  2. 饼图：各部门人数占比")
print("  3. 散点图：年龄与成绩关系")
print("  4. 箱线图：各部门成绩分布")

# ===== 导出结果 =====
print(f"\n【步骤7】导出结果")
print("-" * 40)
df_clean.to_csv('analysis_result.csv', index=False, encoding='utf-8-sig')
print("[OK] 分析结果已保存至 analysis_result.csv")

print("\n" + "=" * 60)
print("                   分析完成！")
print("=" * 60)
