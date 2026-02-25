#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量处理工具
提供文件批量重命名、复制、移动等功能
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class FileBatchProcessor:
    """文件批量处理类"""
    
    def __init__(self, base_dir: str = "."):
        """
        初始化文件处理器
        
        Args:
            base_dir: 基础目录路径
        """
        self.base_dir = Path(base_dir)
        self.processed_files = []
        self.errors = []
    
    def find_files(self, pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        查找匹配模式的文件
        
        Args:
            pattern: 文件匹配模式（如 *.txt）
            recursive: 是否递归查找子目录
            
        Returns:
            匹配的文件路径列表
        """
        if recursive:
            return list(self.base_dir.rglob(pattern))
        else:
            return list(self.base_dir.glob(pattern))
    
    def batch_rename(self, files: List[Path], prefix: str = "", suffix: str = "", 
                    start_number: int = 1, preserve_ext: bool = True) -> int:
        """
        批量重命名文件
        
        Args:
            files: 要重命名的文件列表
            prefix: 文件名前缀
            suffix: 文件名后缀
            start_number: 起始编号
            preserve_ext: 是否保留原文件扩展名
            
        Returns:
            成功重命名的文件数量
        """
        success_count = 0
        
        for idx, file_path in enumerate(files, start=start_number):
            if not file_path.exists():
                self.errors.append(f"文件不存在: {file_path}")
                continue
            
            try:
                # 构建新文件名
                if preserve_ext:
                    new_name = f"{prefix}{idx}{suffix}{file_path.suffix}"
                else:
                    new_name = f"{prefix}{idx}{suffix}"
                
                new_path = file_path.parent / new_name
                
                # 避免重名
                if new_path.exists():
                    self.errors.append(f"目标文件已存在: {new_path}")
                    continue
                
                # 重命名
                file_path.rename(new_path)
                self.processed_files.append({
                    "old_path": str(file_path),
                    "new_path": str(new_path),
                    "operation": "rename"
                })
                success_count += 1
                
            except Exception as e:
                self.errors.append(f"重命名失败 {file_path}: {e}")
        
        return success_count
    
    def batch_copy(self, files: List[Path], dest_dir: str, 
                   preserve_structure: bool = False) -> int:
        """
        批量复制文件
        
        Args:
            files: 要复制的文件列表
            dest_dir: 目标目录
            preserve_structure: 是否保留目录结构
            
        Returns:
            成功复制的文件数量
        """
        success_count = 0
        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            if not file_path.exists():
                self.errors.append(f"文件不存在: {file_path}")
                continue
            
            try:
                if preserve_structure:
                    # 保留相对路径结构
                    rel_path = file_path.relative_to(self.base_dir)
                    new_path = dest_path / rel_path
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    # 只复制文件名
                    new_path = dest_path / file_path.name
                
                shutil.copy2(file_path, new_path)
                self.processed_files.append({
                    "source": str(file_path),
                    "destination": str(new_path),
                    "operation": "copy"
                })
                success_count += 1
                
            except Exception as e:
                self.errors.append(f"复制失败 {file_path}: {e}")
        
        return success_count
    
    def batch_move(self, files: List[Path], dest_dir: str) -> int:
        """
        批量移动文件
        
        Args:
            files: 要移动的文件列表
            dest_dir: 目标目录
            
        Returns:
            成功移动的文件数量
        """
        success_count = 0
        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            if not file_path.exists():
                self.errors.append(f"文件不存在: {file_path}")
                continue
            
            try:
                new_path = dest_path / file_path.name
                shutil.move(str(file_path), str(new_path))
                self.processed_files.append({
                    "source": str(file_path),
                    "destination": str(new_path),
                    "operation": "move"
                })
                success_count += 1
                
            except Exception as e:
                self.errors.append(f"移动失败 {file_path}: {e}")
        
        return success_count
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        获取文件详细信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        if not file_path.exists():
            return {"error": "文件不存在"}
        
        stat = file_path.stat()
        return {
            "name": file_path.name,
            "path": str(file_path),
            "size": stat.st_size,
            "size_human": self._format_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "is_file": file_path.is_file(),
            "extension": file_path.suffix
        }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def generate_report(self) -> str:
        """生成处理报告"""
        report = []
        report.append("=" * 60)
        report.append("文件批量处理报告")
        report.append("=" * 60)
        report.append(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"基础目录: {self.base_dir}")
        report.append("")
        
        if self.processed_files:
            report.append(f"成功处理文件数: {len(self.processed_files)}")
            report.append("")
            report.append("处理详情:")
            for idx, item in enumerate(self.processed_files, 1):
                report.append(f"  {idx}. {item['operation']}:")
                if 'old_path' in item:
                    report.append(f"     {item['old_path']} -> {item['new_path']}")
                else:
                    report.append(f"     {item['source']} -> {item['destination']}")
        else:
            report.append("没有处理任何文件")
        
        if self.errors:
            report.append("")
            report.append(f"错误数: {len(self.errors)}")
            report.append("错误详情:")
            for idx, error in enumerate(self.errors, 1):
                report.append(f"  {idx}. {error}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """主函数 - 演示文件批量处理功能"""
    print("=" * 60)
    print("文件批量处理工具")
    print("=" * 60)
    print()
    
    # 创建处理器实例
    processor = FileBatchProcessor(".")
    
    # 查找所有Python文件
    print("查找Python文件...")
    py_files = processor.find_files("*.py")
    print(f"找到 {len(py_files)} 个Python文件")
    print()
    
    # 显示前5个文件的信息
    print("文件信息示例（前5个）:")
    for file_path in py_files[:5]:
        info = processor.get_file_info(file_path)
        print(f"  {info['name']}: {info['size_human']}, 修改于 {info['modified']}")
    print()
    
    # 查找所有文本文件
    print("查找文本文件...")
    txt_files = processor.find_files("*.txt")
    print(f"找到 {len(txt_files)} 个文本文件")
    print()
    
    # 生成报告
    print(processor.generate_report())
    
    # 保存报告到文件
    report_file = "file_processing_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(processor.generate_report())
    print(f"报告已保存到: {report_file}")


if __name__ == "__main__":
    main()
