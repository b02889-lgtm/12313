---
name: data-analysis-helper
description: 数据分析助手技能。当用户需要以下功能时使用：(1) 分析CSV/JSON数据文件、(2) 计算数据统计指标（平均值、标准差、相关性等）、(3) 数据清洗和预处理、(4) 生成数据可视化建议、(5) 数据转换和格式化、(6) 执行数据探索性分析(EDA)。本技能专注于Python数据分析，使用pandas、numpy等工具处理结构化数据。
---

# 数据分析助手

本技能帮助用户进行数据分析任务，支持CSV、JSON等格式的数据文件。

## 核心功能

### 1. 数据加载与查看

使用pandas加载数据文件：

```python
import pandas as pd

# 加载CSV
df = pd.read_csv('data.csv')

# 加载JSON
df = pd.read_json('data.json')

# 查看基本信息
print(df.head())      # 前5行
print(df.info())      # 数据类型和非空值
print(df.describe())  # 统计摘要
```

### 2. 数据清洗

常见清洗操作：

```python
# 处理缺失值
df.dropna()                    # 删除缺失值
df.fillna(0)                   # 填充为0
df.fillna(df.mean())           # 用均值填充

# 删除重复行
df.drop_duplicates()

# 重命名列
df.rename(columns={'old': 'new'})

# 类型转换
df['column'] = df['column'].astype('float')
```

### 3. 统计分析

常用统计方法：

```python
# 基本统计
df['column'].mean()      # 平均值
df['column'].median()    # 中位数
df['column'].std()       # 标准差
df['column'].min()       # 最小值
df['column'].max()       # 最大值
df['column'].sum()       # 求和

# 分组统计
df.groupby('category')['value'].mean()
df.groupby('category').agg(['mean', 'std', 'count'])

# 相关性分析
df.corr()                # 相关系数矩阵
```

### 4. 数据筛选与查询

```python
# 条件筛选
df[df['age'] > 18]
df[(df['age'] > 18) & (df['gender'] == 'M')]

# 排序
df.sort_values('column', ascending=False)

# 选择特定列
df[['col1', 'col2']]
```

### 5. 数据导出

```python
# 导出为CSV
df.to_csv('output.csv', index=False)

# 导出为JSON
df.to_json('output.json', orient='records')
```

## 工作流程

1. **加载数据**：使用pandas读取文件
2. **探索数据**：查看数据结构和基本统计
3. **清洗数据**：处理缺失值、重复值、类型转换
4. **分析数据**：执行统计计算、分组分析、相关性分析
5. **输出结果**：生成报告或导出处理后的数据

## 最佳实践

- 始终在操作前备份原始数据
- 使用`df.copy()`创建数据副本进行修改
- 处理大数据集时，先采样查看（`df.sample(1000)`）
- 使用`inplace=True`参数直接修改原数据（谨慎使用）

## 依赖库

- pandas: 数据处理和分析
- numpy: 数值计算
- matplotlib/seaborn: 数据可视化（可选）
