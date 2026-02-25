# 数据分析工作流

## 概述

本工作流用于指导完成数据分析任务，包括数据加载、清洗、分析和可视化。

## 工作流步骤

### 1. 数据准备

- [ ] 确定数据源文件路径
- [ ] 检查数据文件格式（CSV、JSON、Excel等）
- [ ] 验证数据文件完整性

### 2. 数据加载

```python
# 使用 pandas 加载数据
import pandas as pd

# 根据文件类型选择合适的加载方法
# CSV 文件
df = pd.read_csv('data.csv')

# JSON 文件
df = pd.read_json('data.json')

# Excel 文件
df = pd.read_excel('data.xlsx')
```

### 3. 数据探索

- [ ] 查看数据基本信息（shape、dtypes、head）
- [ ] 检查缺失值
- [ ] 查看统计摘要
- [ ] 识别异常值

```python
# 数据探索代码示例
print(f"数据形状: {df.shape}")
print(f"\n数据类型:\n{df.dtypes}")
print(f"\n前5行数据:\n{df.head()}")
print(f"\n缺失值统计:\n{df.isnull().sum()}")
print(f"\n统计摘要:\n{df.describe()}")
```

### 4. 数据清洗

- [ ] 处理缺失值（删除或填充）
- [ ] 处理重复数据
- [ ] 数据类型转换
- [ ] 处理异常值

```python
# 数据清洗示例
# 删除缺失值
df_clean = df.dropna()

# 或填充缺失值
df_clean = df.fillna(df.mean())

# 删除重复数据
df_clean = df_clean.drop_duplicates()

# 数据类型转换
df_clean['date_column'] = pd.to_datetime(df_clean['date_column'])
```

### 5. 数据分析

- [ ] 计算基本统计指标（均值、中位数、标准差等）
- [ ] 执行相关性分析
- [ ] 进行分组聚合分析
- [ ] 应用高级分析方法（如需要）

```python
# 基本统计分析
mean_value = df_clean['column_name'].mean()
median_value = df_clean['column_name'].median()
std_value = df_clean['column_name'].std()

# 相关性分析
correlation_matrix = df_clean.corr()

# 分组聚合
grouped_data = df_clean.groupby('category_column').agg({
    'value_column': ['mean', 'sum', 'count']
})
```

### 6. 数据可视化

- [ ] 选择合适的图表类型
- [ ] 创建数据可视化
- [ ] 添加图表标题和标签
- [ ] 保存可视化结果

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表
plt.figure(figsize=(10, 6))
sns.barplot(data=df_clean, x='category', y='value')
plt.title('数据分析结果')
plt.xlabel('类别')
plt.ylabel('数值')
plt.savefig('analysis_result.png')
plt.show()
```

### 7. 生成报告

- [ ] 总结分析结果
- [ ] 提取关键洞察
- [ ] 生成分析报告
- [ ] 保存结果文件

```python
# 生成分析报告
report = f"""
数据分析报告
================
数据集大小: {df_clean.shape[0]} 行, {df_clean.shape[1]} 列
分析时间: {pd.Timestamp.now()}

关键统计:
- 均值: {mean_value:.2f}
- 中位数: {median_value:.2f}
- 标准差: {std_value:.2f}

主要发现:
[在此添加分析发现]
"""

# 保存报告
with open('data_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
```

## 常用命令

```bash
# 运行数据分析脚本
python data_analysis.py

# 安装必要的依赖
pip install pandas numpy matplotlib seaborn

# 查看帮助
python data_analysis.py --help
```

## 注意事项

- 始终保留原始数据副本
- 记录数据清洗的每个步骤
- 验证分析结果的合理性
- 定期保存中间结果
- 使用版本控制管理分析脚本

## 输出文件

- `data_cleaned.csv` - 清洗后的数据
- `analysis_result.png` - 可视化结果
- `data_analysis_report.txt` - 分析报告
- `analysis_summary.json` - 分析摘要（可选）
