#!/usr/bin/env python3
"""
文件整理脚本 - 按文件类型自动分类
"""

import os
import shutil
import sys
from pathlib import Path

# 文件类型分类映射
FILE_CATEGORIES = {
    '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    '文档': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.md', '.csv'],
    '视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
    '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'],
    '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz'],
    '代码': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml', '.yaml', '.yml', '.sql', '.php', '.rb', '.go', '.rs'],
    '可执行文件': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
}


def get_category(filename):
    """根据文件名判断所属分类"""
    ext = Path(filename).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return '其他'


def organize_files(target_path, dry_run=True):
    """
    整理目标文件夹中的文件
    
    Args:
        target_path: 目标文件夹路径
        dry_run: 如果为True，只显示预览不执行
    """
    target_path = Path(target_path).resolve()
    
    if not target_path.exists():
        print(f"错误: 路径不存在 - {target_path}")
        return
    
    if not target_path.is_dir():
        print(f"错误: 不是文件夹 - {target_path}")
        return
    
    # 收集文件信息
    files_to_move = []
    for item in target_path.iterdir():
        if item.is_file():
            category = get_category(item.name)
            files_to_move.append({
                'source': item,
                'category': category,
                'target_dir': target_path / category
            })
    
    if not files_to_move:
        print("没有找到需要整理的文件。")
        return
    
    # 显示预览
    print(f"\n{'='*60}")
    print(f"文件整理预览 (目标: {target_path})")
    print(f"{'='*60}\n")
    
    # 按分类分组显示
    by_category = {}
    for item in files_to_move:
        cat = item['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item['source'].name)
    
    for category, files in sorted(by_category.items()):
        print(f"\n[{category}] -> 文件夹: {category}/")
        for f in files[:5]:  # 最多显示5个
            print(f"  - {f}")
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个文件")
    
    print(f"\n{'='*60}")
    print(f"总计: {len(files_to_move)} 个文件将被整理到 {len(by_category)} 个分类文件夹")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("这是预览模式，未执行任何操作。")
        print("要实际执行，请添加 --execute 参数")
        return
    
    # 执行移动
    print("开始执行文件整理...")
    moved_count = 0
    
    for item in files_to_move:
        try:
            # 创建目标文件夹
            item['target_dir'].mkdir(exist_ok=True)
            
            # 移动文件
            target_file = item['target_dir'] / item['source'].name
            
            # 如果目标文件已存在，添加数字后缀
            counter = 1
            original_target = target_file
            while target_file.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_file = original_target.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.move(str(item['source']), str(target_file))
            moved_count += 1
            print(f"✓ {item['source'].name} -> {item['category']}/")
            
        except Exception as e:
            print(f"✗ 移动失败 {item['source'].name}: {e}")
    
    print(f"\n完成! 成功移动 {moved_count}/{len(files_to_move)} 个文件。")


def main():
    if len(sys.argv) < 2:
        print("用法: python organize_by_type.py <文件夹路径> [--execute]")
        print("\n示例:")
        print("  python organize_by_type.py ~/Downloads      # 预览模式")
        print("  python organize_by_type.py ~/Downloads --execute  # 执行整理")
        sys.exit(1)
    
    target_path = sys.argv[1]
    dry_run = '--execute' not in sys.argv
    
    organize_files(target_path, dry_run)


if __name__ == '__main__':
    main()
