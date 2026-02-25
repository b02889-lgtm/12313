#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理和分析脚本
支持CSV、Excel文件的数据读取、清洗、分析和可视化
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import sys

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class DataAnalyzer:
    """数据分析器类"""
    
    def __init__(self, filepath=None):
        """
        初始化数据分析器
        
        Args:
            filepath: 数据文件路径（CSV或Excel）
        """
        self.data = None
        self.filepath = filepath
        if filepath:
            self.load_data(filepath)
    
    def load_data(self, filepath):
        """
        加载数据文件
        
        Args:
            filepath: 数据文件路径
        """
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {filepath}")
            
            # 根据文件扩展名选择读取方式
            if file_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(filepath, encoding='utf-8')
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(filepath)
            else:
                raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
            print(f"✓ 成功加载数据: {filepath}")
            print(f"  数据形状: {self.data.shape}")
            print(f"  列名: {list(self.data.columns)}")
            
        except Exception as e:
            print(f"✗ 加载数据失败: {str(e)}")
            raise
    
    def get_basic_info(self):
        """获取数据基本信息"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据基本信息")
        print("="*60)
        print(f"数据形状: {self.data.shape[0]} 行 × {self.data.shape[1]} 列")
        print(f"内存使用: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print("\n数据类型:")
        print(self.data.dtypes)
        print("\n前5行数据:")
        print(self.data.head())
        print("\n后5行数据:")
        print(self.data.tail())
    
    def get_statistics(self):
        """获取数据统计信息"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据统计信息")
        print("="*60)
        
        # 数值型数据统计
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print("\n数值型数据统计:")
            print(self.data[numeric_cols].describe())
        
        # 分类数据统计
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print("\n分类数据统计:")
            for col in categorical_cols:
                print(f"\n{col}:")
                print(self.data[col].value_counts().head(10))
    
    def check_missing_values(self):
        """检查缺失值"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("缺失值检查")
        print("="*60)
        
        missing = self.data.isnull().sum()
        missing_percent = (missing / len(self.data)) * 100
        
        missing_df = pd.DataFrame({
            '缺失数量': missing,
            '缺失比例(%)': missing_percent
        })
        
        missing_df = missing_df[missing_df['缺失数量'] > 0]
        
        if len(missing_df) > 0:
            print(missing_df)
        else:
            print("✓ 数据中没有缺失值")
    
    def clean_data(self, drop_na=False, fill_method='mean'):
        """
        数据清洗
        
        Args:
            drop_na: 是否删除包含缺失值的行
            fill_method: 填充缺失值的方法 ('mean', 'median', 'mode', 'forward', 'backward')
        """
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据清洗")
        print("="*60)
        
        original_shape = self.data.shape
        
        if drop_na:
            self.data = self.data.dropna()
            print(f"✓ 删除缺失值后数据形状: {self.data.shape}")
        else:
            # 填充缺失值
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            
            # 填充数值型数据
            if len(numeric_cols) > 0:
                if fill_method == 'mean':
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].mean())
                elif fill_method == 'median':
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].median())
                elif fill_method == 'forward':
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(method='ffill')
                elif fill_method == 'backward':
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(method='bfill')
            
            # 填充分类数据
            if len(categorical_cols) > 0:
                self.data[categorical_cols] = self.data[categorical_cols].fillna('未知')
            
            print(f"✓ 使用 {fill_method} 方法填充缺失值")
        
        print(f"原始数据: {original_shape[0]} 行")
        print(f"清洗后数据: {self.data.shape[0]} 行")
        print(f"删除/修改: {original_shape[0] - self.data.shape[0]} 行")
    
    def analyze_correlation(self):
        """分析数据相关性"""
        if self.data is None:
            print("请先加载数据")
            return
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("数值型列少于2个，无法计算相关性")
            return
        
        print("\n" + "="*60)
        print("相关性分析")
        print("="*60)
        
        correlation = self.data[numeric_cols].corr()
        print(correlation)
        
        # 绘制相关性热力图
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
        plt.title('数据相关性热力图')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("\n✓ 相关性热力图已保存为: correlation_heatmap.png")
        plt.close()
    
    def visualize_data(self):
        """数据可视化"""
        if self.data is None:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据可视化")
        print("="*60)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        
        # 数值型数据分布
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.ravel()
            
            for i, col in enumerate(numeric_cols[:4]):
                if i < 4:
                    self.data[col].hist(bins=30, ax=axes[i])
                    axes[i].set_title(f'{col} 分布')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('频数')
            
            plt.tight_layout()
            plt.savefig('numeric_distribution.png', dpi=300, bbox_inches='tight')
            print("✓ 数值型数据分布图已保存为: numeric_distribution.png")
            plt.close()
        
        # 分类数据统计
        if len(categorical_cols) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.ravel()
            
            for i, col in enumerate(categorical_cols[:4]):
                if i < 4:
                    self.data[col].value_counts().head(10).plot(kind='bar', ax=axes[i])
                    axes[i].set_title(f'{col} 统计')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('数量')
                    axes[i].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('categorical_stats.png', dpi=300, bbox_inches='tight')
            print("✓ 分类数据统计图已保存为: categorical_stats.png")
            plt.close()
    
    def export_results(self, output_file='analysis_results.xlsx'):
        """
        导出分析结果
        
        Args:
            output_file: 输出文件名
        """
        if self.data is None:
            print("请先加载数据")
            return
        
        try:
            # 创建Excel写入器
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 原始数据
                self.data.to_excel(writer, sheet_name='原始数据', index=False)
                
                # 统计信息
                numeric_cols = self.data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    self.data[numeric_cols].describe().to_excel(writer, sheet_name='统计信息')
                
                # 缺失值信息
                missing = self.data.isnull().sum()
                missing_df = pd.DataFrame({
                    '缺失数量': missing,
                    '缺失比例(%)': (missing / len(self.data)) * 100
                })
                missing_df.to_excel(writer, sheet_name='缺失值信息')
            
            print(f"\n✓ 分析结果已导出为: {output_file}")
            
        except Exception as e:
            print(f"✗ 导出失败: {str(e)}")
    
    def generate_report(self):
        """生成分析报告"""
        if self.data is None:
            print("请先加载数据")
            return
        
        report = {
            '数据文件': str(self.filepath) if self.filepath else '未指定',
            '数据形状': {'行数': int(self.data.shape[0]), '列数': int(self.data.shape[1])},
            '列名': list(self.data.columns),
            '数据类型': {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            '缺失值': {col: int(count) for col, count in self.data.isnull().sum().items() if count > 0},
            '数值型列': list(self.data.select_dtypes(include=[np.number]).columns),
            '分类列': list(self.data.select_dtypes(include=['object']).columns)
        }
        
        # 保存为JSON
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n✓ 分析报告已保存为: analysis_report.json")
        
        return report


def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'ID': range(1, n_samples + 1),
        '姓名': [f'用户{i}' for i in range(1, n_samples + 1)],
        '年龄': np.random.randint(18, 65, n_samples),
        '性别': np.random.choice(['男', '女'], n_samples),
        '城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州'], n_samples),
        '收入': np.random.normal(10000, 3000, n_samples),
        '消费': np.random.normal(5000, 1500, n_samples),
        '评分': np.random.uniform(1, 5, n_samples),
        '会员等级': np.random.choice(['普通', '银卡', '金卡', '钻石'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # 添加一些缺失值
    df.loc[np.random.choice(df.index, 50), '收入'] = np.nan
    df.loc[np.random.choice(df.index, 30), '消费'] = np.nan
    
    df.to_csv('sample_data.csv', index=False, encoding='utf-8-sig')
    print("✓ 示例数据已创建: sample_data.csv")
    
    return 'sample_data.csv'


def main():
    """主函数"""
    print("="*60)
    print("数据分析脚本")
    print("="*60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # 创建示例数据
        filepath = create_sample_data()
    
    try:
        # 创建分析器
        analyzer = DataAnalyzer(filepath)
        
        # 执行分析
        analyzer.get_basic_info()
        analyzer.check_missing_values()
        analyzer.get_statistics()
        
        # 数据清洗
        analyzer.clean_data(fill_method='mean')
        
        # 相关性分析
        analyzer.analyze_correlation()
        
        # 数据可视化
        analyzer.visualize_data()
        
        # 导出结果
        analyzer.export_results()
        
        # 生成报告
        analyzer.generate_report()
        
        print("\n" + "="*60)
        print("✓ 数据分析完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ 分析过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()