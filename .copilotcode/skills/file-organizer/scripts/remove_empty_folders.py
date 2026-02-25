#!/usr/bin/env python3
"""
清理空文件夹脚本
"""

import os
import sys
from pathlib import Path


def remove_empty_folders(folder_path, recursive=False, dry_run=True):
    """
    删除空文件夹
    
    Args:
        folder_path: 目标文件夹路径
        recursive: 是否递归删除子文件夹中的空文件夹
        dry_run: 如果为True，只显示预览不执行
    """
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"错误: 无效的文件夹路径 - {folder_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"查找空文件夹 (文件夹: {folder_path})")
    print(f"递归搜索: {'是' if recursive else '否'}")
    print(f"{'='*60}\n")
    
    # 收集空文件夹
    empty_folders = []
    
    if recursive:
        # 从深层到浅层遍历，确保先处理子文件夹
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if is_empty_folder(dir_path):
                    empty_folders.append(dir_path)
    else:
        # 只检查直接子文件夹
        for item in folder_path.iterdir():
            if item.is_dir() and is_empty_folder(item):
                empty_folders.append(item)
    
    if not empty_folders:
        print("✓ 没有发现空文件夹。")
        return
    
    # 显示空文件夹列表
    print(f"发现 {len(empty_folders)} 个空文件夹:\n")
    for i, folder in enumerate(empty_folders, 1):
        print(f"  [{i}] {folder}")
    
    print(f"\n{'='*60}")
    print(f"总计: {len(empty_folders)} 个空文件夹将被删除")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("这是预览模式，未执行任何操作。")
        print("要实际执行，请添加 --execute 参数")
        return
    
    # 执行删除
    print("开始删除空文件夹...")
    success_count = 0
    
    for folder in empty_folders:
        try:
            folder.rmdir()
            success_count += 1
            print(f"✓ 已删除: {folder}")
        except Exception as e:
            print(f"✗ 删除失败 {folder}: {e}")
    
    print(f"\n完成! 成功删除 {success_count}/{len(empty_folders)} 个空文件夹。")


def is_empty_folder(folder_path):
    """检查文件夹是否为空"""
    try:
        return not any(folder_path.iterdir())
    except Exception:
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python remove_empty_folders.py <文件夹路径> [--recursive] [--execute]")
        print("\n示例:")
        print("  python remove_empty_folders.py ~/Downloads")
        print("  python remove_empty_folders.py ~/Documents --recursive --execute")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    recursive = '--recursive' in sys.argv or '-r' in sys.argv
    dry_run = '--execute' not in sys.argv
    
    remove_empty_folders(folder_path, recursive, dry_run)


if __name__ == '__main__':
    main()
