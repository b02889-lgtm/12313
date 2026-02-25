#!/usr/bin/env python3
"""
批量重命名文件脚本
"""

import os
import sys
import re
from pathlib import Path


def batch_rename(folder_path, pattern, start_number=1, dry_run=True):
    """
    批量重命名文件夹中的文件
    
    Args:
        folder_path: 目标文件夹路径
        pattern: 命名模式，使用 {:03d} 表示数字序号
        start_number: 起始编号
        dry_run: 如果为True，只显示预览不执行
    """
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"错误: 无效的文件夹路径 - {folder_path}")
        return
    
    # 获取所有文件（不包括子文件夹）
    files = [f for f in folder_path.iterdir() if f.is_file()]
    files.sort()  # 按名称排序
    
    if not files:
        print("文件夹中没有文件。")
        return
    
    # 检查模式中是否包含序号占位符
    if '{:' not in pattern:
        print("警告: 命名模式中不包含序号占位符（如 {:03d}），所有文件将被命名为相同名称。")
    
    print(f"\n{'='*60}")
    print(f"批量重命名预览 (文件夹: {folder_path})")
    print(f"{'='*60}\n")
    
    rename_plan = []
    for i, file in enumerate(files, start=start_number):
        # 保留原文件扩展名
        if '{:' in pattern:
            # 用户提供了带占位符的模式
            new_name = pattern.format(i)
            # 如果模式没有扩展名，保留原扩展名
            if '.' not in pattern or pattern.endswith('}'):
                new_name += file.suffix
        else:
            # 简单模式，添加序号前缀避免冲突
            new_name = f"{pattern}_{i:03d}{file.suffix}"
        
        new_path = folder_path / new_name
        
        rename_plan.append({
            'old': file.name,
            'new': new_name,
            'old_path': file,
            'new_path': new_path
        })
        
        print(f"{file.name:<40} -> {new_name}")
    
    print(f"\n{'='*60}")
    print(f"总计: {len(rename_plan)} 个文件将被重命名")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("这是预览模式，未执行任何操作。")
        print("要实际执行，请添加 --execute 参数")
        return
    
    # 执行重命名
    print("开始执行重命名...")
    success_count = 0
    
    for item in rename_plan:
        try:
            # 检查目标文件是否已存在
            if item['new_path'].exists():
                print(f"✗ 跳过 {item['old']}: 目标文件已存在")
                continue
            
            item['old_path'].rename(item['new_path'])
            success_count += 1
            print(f"✓ {item['old']} -> {item['new']}")
        except Exception as e:
            print(f"✗ 重命名失败 {item['old']}: {e}")
    
    print(f"\n完成! 成功重命名 {success_count}/{len(rename_plan)} 个文件。")


def main():
    if len(sys.argv) < 3:
        print("用法: python batch_rename.py <文件夹路径> <命名模式> [--execute] [--start N]")
        print("\n命名模式示例:")
        print("  'photo_{:03d}'      -> photo_001.jpg, photo_002.jpg, ...")
        print("  'doc_{:04d}.pdf'    -> doc_0001.pdf, doc_0002.pdf, ...")
        print("  'file_{:02d}'       -> file_01.txt, file_02.txt, ...")
        print("\n示例:")
        print("  python batch_rename.py ./photos 'vacation_{:03d}' --execute")
        print("  python batch_rename.py ./docs 'report_{:02d}.pdf' --execute --start 5")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    pattern = sys.argv[2]
    dry_run = '--execute' not in sys.argv
    
    # 解析起始编号
    start_number = 1
    for i, arg in enumerate(sys.argv):
        if arg == '--start' and i + 1 < len(sys.argv):
            try:
                start_number = int(sys.argv[i + 1])
            except ValueError:
                print(f"警告: 无效的起始编号，使用默认值 1")
    
    batch_rename(folder_path, pattern, start_number, dry_run)


if __name__ == '__main__':
    main()
