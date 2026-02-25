#!/usr/bin/env python3
"""
查找重复文件脚本
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict


def calculate_file_hash(file_path, chunk_size=8192):
    """计算文件的MD5哈希值"""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"警告: 无法读取文件 {file_path}: {e}")
        return None


def find_duplicates(folder_path, recursive=False):
    """
    查找文件夹中的重复文件
    
    Args:
        folder_path: 目标文件夹路径
        recursive: 是否递归搜索子文件夹
    """
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"错误: 无效的文件夹路径 - {folder_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"查找重复文件 (文件夹: {folder_path})")
    print(f"递归搜索: {'是' if recursive else '否'}")
    print(f"{'='*60}\n")
    
    # 收集所有文件
    files = []
    if recursive:
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.is_file():
                    files.append(file_path)
    else:
        files = [f for f in folder_path.iterdir() if f.is_file()]
    
    if not files:
        print("没有找到文件。")
        return
    
    print(f"正在扫描 {len(files)} 个文件...\n")
    
    # 计算哈希值并分组
    hash_groups = defaultdict(list)
    for file_path in files:
        file_hash = calculate_file_hash(file_path)
        if file_hash:
            hash_groups[file_hash].append(file_path)
    
    # 找出重复的文件
    duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    if not duplicates:
        print("✓ 没有发现重复文件。")
        return
    
    # 显示重复文件
    print(f"发现 {len(duplicates)} 组重复文件:\n")
    
    total_duplicates = 0
    total_size = 0
    
    for i, (file_hash, files) in enumerate(duplicates.items(), 1):
        print(f"{'='*60}")
        print(f"重复组 #{i} (哈希: {file_hash[:16]}...)")
        print(f"{'='*60}")
        
        for j, file_path in enumerate(files):
            size = file_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"  [{j+1}] {file_path}")
            print(f"      大小: {size:,} 字节 ({size_mb:.2f} MB)")
        
        # 计算可节省的空间
        duplicate_size = files[0].stat().st_size
        saved_space = duplicate_size * (len(files) - 1)
        total_size += saved_space
        total_duplicates += len(files) - 1
        
        print(f"\n  可节省空间: {saved_space:,} 字节 ({saved_space/(1024*1024):.2f} MB)")
        print()
    
    print(f"{'='*60}")
    print(f"总计: {total_duplicates} 个重复文件")
    print(f"可节省空间: {total_size:,} 字节 ({total_size/(1024*1024):.2f} MB)")
    print(f"{'='*60}\n")
    
    print("提示: 手动检查并删除不需要的重复文件。")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python find_duplicates.py <文件夹路径> [--recursive]")
        print("\n示例:")
        print("  python find_duplicates.py ~/Downloads")
        print("  python find_duplicates.py ~/Documents --recursive")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    recursive = '--recursive' in sys.argv or '-r' in sys.argv
    
    find_duplicates(folder_path, recursive)


if __name__ == '__main__':
    main()
