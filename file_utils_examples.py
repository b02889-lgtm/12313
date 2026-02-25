#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
file_utils.py 使用示例
演示如何使用文件处理工具的各种功能
"""

from file_utils import FileUtils


def example_list_files():
    """示例：列出文件"""
    print("=" * 50)
    print("示例1：列出所有Python文件")
    print("=" * 50)
    
    utils = FileUtils(".")
    files = utils.list_files("*.py")
    
    print(f"找到 {len(files)} 个Python文件:")
    for f in files:
        print(f"  - {f.name}")
    print()


def example_batch_rename():
    """示例：批量重命名文件"""
    print("=" * 50)
    print("示例2：批量重命名文件（预览模式）")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 预览：将所有 .txt 文件中的 "新建" 替换为 "new"
    results = utils.batch_rename(
        pattern="新建",
        replacement="new",
        file_pattern="*.txt",
        dry_run=True
    )
    
    print("预览重命名结果:")
    for r in results:
        print(f"  [{r['status']}] {r['message']}")
    print()


def example_csv_to_json():
    """示例：CSV转JSON"""
    print("=" * 50)
    print("示例3：CSV文件转JSON文件")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 假设有一个 sample_data.csv 文件
    result = utils.convert_csv_to_json("sample_data.csv", "sample_data_converted.json")
    
    print(f"[{result['status']}] {result['message']}")
    if result['status'] == 'success':
        print(f"  转换了 {result['records']} 条记录")
    print()


def example_json_to_csv():
    """示例：JSON转CSV"""
    print("=" * 50)
    print("示例4：JSON文件转CSV文件")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 假设有一个 sample_data.json 文件
    result = utils.convert_json_to_csv("sample_data.json", "sample_data_converted.csv")
    
    print(f"[{result['status']}] {result['message']}")
    if result['status'] == 'success':
        print(f"  转换了 {result['records']} 条记录")
    print()


def example_process_text():
    """示例：处理文本文件"""
    print("=" * 50)
    print("示例5：处理文本文件内容")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 定义一个处理函数：将所有空行删除
    def remove_empty_lines(text):
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        return '\n'.join(non_empty_lines)
    
    # 处理文件
    result = utils.process_text_file(
        "example_code.py",
        processor=remove_empty_lines,
        output_file="example_code_cleaned.py"
    )
    
    print(f"[{result['status']}] {result['message']}")
    if result['status'] == 'success':
        print(f"  原始大小: {result['original_size']} 字符")
        print(f"  处理后大小: {result['processed_size']} 字符")
    print()


def example_merge_files():
    """示例：合并文件"""
    print("=" * 50)
    print("示例6：合并多个文本文件")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 合并所有 .md 文件
    result = utils.merge_files(
        file_pattern="*.md",
        output_file="all_docs_merged.md",
        separator="\n\n---\n\n"
    )
    
    print(f"[{result['status']}] {result['message']}")
    if result['status'] == 'success':
        print(f"  合并了 {result['total_files']} 个文件")
        print(f"  总大小: {result['total_size']} 字符")
    print()


def example_file_info():
    """示例：获取文件信息"""
    print("=" * 50)
    print("示例7：获取文件详细信息")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 获取文件信息
    info = utils.get_file_info("file_utils.py")
    
    if info['status'] == 'success':
        print(f"文件名: {info['name']}")
        print(f"完整路径: {info['path']}")
        print(f"文件大小: {info['size_human']}")
        print(f"创建时间: {info['created']}")
        print(f"修改时间: {info['modified']}")
        print(f"文件类型: {'文件' if info['is_file'] else '目录'}")
        print(f"扩展名: {info['extension']}")
    else:
        print(f"[{info['status']}] {info['message']}")
    print()


def example_custom_processor():
    """示例：自定义文本处理器"""
    print("=" * 50)
    print("示例8：自定义文本处理器")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 定义一个处理函数：统计并添加行号
    def add_line_numbers(text):
        lines = text.split('\n')
        numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered_lines)
    
    # 处理文件
    result = utils.process_text_file(
        "hello_world.py",
        processor=add_line_numbers,
        output_file="hello_world_numbered.py"
    )
    
    print(f"[{result['status']}] {result['message']}")
    print()


def example_recursive_search():
    """示例：递归搜索文件"""
    print("=" * 50)
    print("示例9：递归搜索文件")
    print("=" * 50)
    
    utils = FileUtils(".")
    
    # 递归搜索所有 .py 文件
    files = utils.list_files("*.py", recursive=True)
    
    print(f"递归搜索找到 {len(files)} 个Python文件:")
    for f in files[:10]:  # 只显示前10个
        print(f"  - {f}")
    if len(files) > 10:
        print(f"  ... 还有 {len(files) - 10} 个文件")
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("FileUtils 工具使用示例")
    print("=" * 50 + "\n")
    
    # 运行各个示例
    example_list_files()
    example_batch_rename()
    example_csv_to_json()
    example_json_to_csv()
    example_process_text()
    example_merge_files()
    example_file_info()
    example_custom_processor()
    example_recursive_search()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)
    print("\n命令行使用示例:")
    print("  python file_utils.py list *.py")
    print("  python file_utils.py rename 'old' 'new' -f '*.txt' --dry-run")
    print("  python file_utils.py csv2json sample_data.csv -o output.json")
    print("  python file_utils.py json2csv sample_data.json -o output.csv")
    print("  python file_utils.py info file_utils.py")
    print()


if __name__ == '__main__':
    main()
