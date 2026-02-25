#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理和分析脚本（简化版）
使用Python标准库，无需安装额外依赖
"""

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
import sys


class SimpleDataAnalyzer:
    """简单数据分析器类（使用标准库）"""
    
    def __init__(self, filepath=None):
        """
        初始化数据分析器
        
        Args:
            filepath: 数据文件路径（CSV）
        """
        self.data = []
        self.headers = []
        self.filepath = filepath
        if filepath:
            self.load_data(filepath)
    
    def load_data(self, filepath):
        """
        加载CSV数据文件
        
        Args:
            filepath: 数据文件路径
        """
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames
                self.data = list(reader)
            
            print(f"✓ 成功加载数据: {filepath}")
            print(f"  数据行数: {len(self.data)}")
            print(f"  列数: {len(self.headers)}")
            print(f"  列名: {self.headers}")
            
        except Exception as e:
            print(f"✗ 加载数据失败: {str(e)}")
            raise
    
    def get_basic_info(self):
        """获取数据基本信息"""
        if not self.data:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据基本信息")
        print("="*60)
        print(f"数据行数: {len(self.data)}")
        print(f"数据列数: {len(self.headers)}")
        print(f"列名: {self.headers}")
        
        print("\n前5行数据:")
        for i, row in enumerate(self.data[:5]):
            print(f"行{i+1}: {row}")
        
        print("\n后5行数据:")
        for i, row in enumerate(self.data[-5:], start=len(self.data)-4):
            print(f"行{i}: {row}")
    
    def get_statistics(self):
        """获取数据统计信息"""
        if not self.data:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据统计信息")
        print("="*60)
        
        # 分析每一列
        for col in self.headers:
            values = [row.get(col, '') for row in self.data]
            
            # 尝试转换为数值
            numeric_values = []
            for val in values:
                try:
                    numeric_values.append(float(val))
                except (ValueError, TypeError):
                    pass
            
            if numeric_values:
                # 数值型数据统计
                print(f"\n【{col}】(数值型)")
                print(f"  有效值数量: {len(numeric_values)}")
                print(f"  缺失值数量: {len(values) - len(numeric_values)}")
                print(f"  最小值: {min(numeric_values):.2f}")
                print(f"  最大值: {max(numeric_values):.2f}")
                print(f"  平均值: {statistics.mean(numeric_values):.2f}")
                print(f"  中位数: {statistics.median(numeric_values):.2f}")
                try:
                    print(f"  标准差: {statistics.stdev(numeric_values):.2f}")
                except statistics.StatisticsError:
                    print(f"  标准差: N/A (数据量不足)")
            else:
                # 分类数据统计
                print(f"\n【{col}】(分类型)")
                counter = Counter(values)
                print(f"  唯一值数量: {len(counter)}")
                print(f"  前10个最常见值:")
                for val, count in counter.most_common(10):
                    print(f"    {val}: {count} 次 ({count/len(values)*100:.1f}%)")
    
    def check_missing_values(self):
        """检查缺失值"""
        if not self.data:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("缺失值检查")
        print("="*60)
        
        missing_info = {}
        for col in self.headers:
            missing_count = sum(1 for row in self.data if not row.get(col))
            missing_percent = (missing_count / len(self.data)) * 100
            missing_info[col] = {
                '缺失数量': missing_count,
                '缺失比例(%)': round(missing_percent, 2)
            }
        
        has_missing = any(info['缺失数量'] > 0 for info in missing_info.values())
        
        if has_missing:
            for col, info in missing_info.items():
                if info['缺失数量'] > 0:
                    print(f"{col}: {info['缺失数量']} 个缺失值 ({info['缺失比例(%)']}%)")
        else:
            print("✓ 数据中没有缺失值")
    
    def clean_data(self, drop_na=False, fill_method='mean'):
        """
        数据清洗
        
        Args:
            drop_na: 是否删除包含缺失值的行
            fill_method: 填充缺失值的方法 ('mean', 'median', 'mode', 'unknown')
        """
        if not self.data:
            print("请先加载数据")
            return
        
        print("\n" + "="*60)
        print("数据清洗")
        print("="*60)
        
        original_count = len(self.data)
        
        if drop_na:
            # 删除包含缺失值的行
            self.data = [row for row in self.data if all(row.get(col) for col in self.headers)]
            print(f"✓ 删除缺失值后数据行数: {len(self.data)}")
        else:
            # 填充缺失值
            for col in self.headers:
                values = [row.get(col) for row in self.data]
                
                # 尝试转换为数值
                numeric_values = []
                for val in values:
                    try:
                        numeric_values.append(float(val))
                    except (ValueError, TypeError):
                        pass
                
                if numeric_values:
                    # 数值型数据
                    if fill_method == 'mean':
                        fill_value = statistics.mean(numeric_values)
                    elif fill_method == 'median':
                        fill_value = statistics.median(numeric_values)
                    else:
                        fill_value = 0
                    
                    for row in self.data:
                        if not row.get(col):
                            row[col] = fill_value
                else:
                    # 分类数据
                    if fill_method == 'mode':
                        counter = Counter(values)
                        fill_value = counter.most_common(1)[0][0] if counter else '未知'
                    else:
                        fill_value = '未知'
                    
                    for row in self.data:
                        if not row.get(col):
                            row[col] = fill_value
            
            print(f"✓ 使用 {fill_method} 方法填充缺失值")
        
        print(f"原始数据: {original_count} 行")
        print(f"清洗后数据: {len(self.data)} 行")
        print(f"删除/修改: {original_count - len(self.data)} 行")
    
    def analyze_correlation(self):
        """分析数据相关性（仅数值型数据）"""
        if not self.data:
            print("请先加载数据")
            return
        
        # 提取数值型列
        numeric_cols = []
        for col in self.headers:
            values = [row.get(col) for row in self.data]
            numeric_values = []
            for val in values:
                try:
                    numeric_values.append(float(val))
                except (ValueError, TypeError):
                    pass
            
            if numeric_values:
                numeric_cols.append(col)
        
        if len(numeric_cols) < 2:
            print("数值型列少于2个，无法计算相关性")
            return
        
        print("\n" + "="*60)
        print("相关性分析")
        print("="*60)
        
        # 计算相关性矩阵
        correlation_matrix = {}
        for col1 in numeric_cols:
            correlation_matrix[col1] = {}
            values1 = [float(row.get(col1, 0)) for row in self.data]
            
            for col2 in numeric_cols:
                values2 = [float(row.get(col2, 0)) for row in self.data]
                
                # 计算皮尔逊相关系数（使用标准库 statistics.correlation，Python 3.10+）
                try:
                    # 使用更精确的统计库函数
                    correlation = statistics.correlation(values1, values2)
                    correlation_matrix[col1][col2] = round(correlation, 3)
                except (statistics.StatisticsError, ValueError):
                    # 数据量不足或标准差为零时
                    correlation_matrix[col1][col2] = 0
                except Exception:
                    # 其他异常情况
                    correlation_matrix[col1][col2] = 0
        
        # 打印相关性矩阵
        print("\n相关性矩阵:")
        print(" " * 15, end="")
        for col in numeric_cols:
            print(f"{col[:10]:>10}", end="")
        print()
        
        for col1 in numeric_cols:
            print(f"{col1[:15]:<15}", end="")
            for col2 in numeric_cols:
                print(f"{correlation_matrix[col1][col2]:>10}", end="")
            print()
    
    def export_results(self, output_file='analysis_results.csv'):
        """
        导出分析结果
        
        Args:
            output_file: 输出文件名
        """
        if not self.data:
            print("请先加载数据")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self.data)
            
            print(f"\n✓ 分析结果已导出为: {output_file}")
            
        except Exception as e:
            print(f"✗ 导出失败: {str(e)}")
    
    def generate_report(self):
        """生成分析报告"""
        if not self.data:
            print("请先加载数据")
            return
        
        # 分析数据类型
        numeric_cols = []
        categorical_cols = []
        
        for col in self.headers:
            values = [row.get(col) for row in self.data]
            numeric_values = []
            for val in values:
                try:
                    numeric_values.append(float(val))
                except (ValueError, TypeError):
                    pass
            
            if numeric_values:
                numeric_cols.append(col)
            else:
                categorical_cols.append(col)
        
        # 统计缺失值
        missing_info = {}
        for col in self.headers:
            missing_count = sum(1 for row in self.data if not row.get(col))
            if missing_count > 0:
                missing_info[col] = missing_count
        
        report = {
            '数据文件': str(self.filepath) if self.filepath else '未指定',
            '数据形状': {
                '行数': len(self.data),
                '列数': len(self.headers)
            },
            '列名': self.headers,
            '数值型列': numeric_cols,
            '分类列': categorical_cols,
            '缺失值': missing_info
        }
        
        # 保存为JSON
        with open('analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n✓ 分析报告已保存为: analysis_report.json")
        
        return report


def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    import random
    
    data = []
    cities = ['北京', '上海', '广州', '深圳', '杭州']
    genders = ['男', '女']
    levels = ['普通', '银卡', '金卡', '钻石']
    
    for i in range(1, 1001):
        row = {
            'ID': i,
            '姓名': f'用户{i}',
            '年龄': random.randint(18, 65),
            '性别': random.choice(genders),
            '城市': random.choice(cities),
            '收入': round(random.gauss(10000, 3000), 2),
            '消费': round(random.gauss(5000, 1500), 2),
            '评分': round(random.uniform(1, 5), 1),
            '会员等级': random.choice(levels)
        }
        
        # 添加一些缺失值
        if random.random() < 0.05:
            row['收入'] = ''
        if random.random() < 0.03:
            row['消费'] = ''
        
        data.append(row)
    
    # 保存为CSV
    with open('sample_data.csv', 'w', encoding='utf-8-sig', newline='') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print("✓ 示例数据已创建: sample_data.csv")
    
    return 'sample_data.csv'


def main():
    """主函数"""
    print("="*60)
    print("数据分析脚本（简化版）")
    print("="*60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        # 创建示例数据
        filepath = create_sample_data()
    
    try:
        # 创建分析器
        analyzer = SimpleDataAnalyzer(filepath)
        
        # 执行分析
        analyzer.get_basic_info()
        analyzer.check_missing_values()
        analyzer.get_statistics()
        
        # 数据清洗
        analyzer.clean_data(fill_method='mean')
        
        # 相关性分析
        analyzer.analyze_correlation()
        
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