"""
XML 标签识别与验证工具
支持：标签识别、嵌套验证、语法检查
"""

import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple


class XMLTagValidator:
    """XML 标签识别与验证器"""
    
    def __init__(self, xml_string: str):
        self.xml_string = xml_string
        self.tags = []
        self._parse_tags()
    
    def _parse_tags(self):
        """解析所有XML标签"""
        # 匹配开始标签、结束标签、自闭合标签
        pattern = r'<(/?)(\w[\w\-.]*)([^>]*?)(/?)>'
        matches = re.finditer(pattern, self.xml_string)
        
        for match in matches:
            closing, tag_name, attrs, self_closing = match.groups()
            tag_info = {
                'type': 'end' if closing else 'self-closing' if self_closing else 'start',
                'name': tag_name,
                'attrs': attrs.strip(),
                'position': match.start(),
                'full_tag': match.group()
            }
            self.tags.append(tag_info)
    
    def print_all_tags(self):
        """打印所有识别到的标签"""
        print("=" * 60)
        print("📋 XML 标签识别结果")
        print("=" * 60)
        
        if not self.tags:
            print("❌ 未找到任何XML标签")
            return
        
        for i, tag in enumerate(self.tags, 1):
            tag_type = {
                'start': '开始标签',
                'end': '结束标签',
                'self-closing': '自闭合标签'
            }[tag['type']]
            
            print(f"\n[{i}] {tag_type}: <{tag['name']}>")
            print(f"    完整标签: {tag['full_tag']}")
            if tag['attrs']:
                print(f"    属性: {tag['attrs']}")
            print(f"    位置: {tag['position']}")
    
    def validate_nesting(self) -> bool:
        """验证标签嵌套是否正确"""
        print("\n" + "=" * 60)
        print("🔍 标签嵌套验证")
        print("=" * 60)
        
        stack = []
        
        for tag in self.tags:
            if tag['type'] == 'self-closing':
                continue
            
            if tag['type'] == 'start':
                stack.append(tag['name'])
            elif tag['type'] == 'end':
                if not stack:
                    print(f"❌ 错误: 结束标签 </{tag['name']}> 没有对应的开始标签")
                    return False
                
                expected = stack[-1]
                if expected != tag['name']:
                    print(f"❌ 错误: 标签 </{tag['name']}> 不匹配，期望 </{expected}>")
                    print(f"   未闭合的标签栈: {stack}")
                    return False
                
                stack.pop()
        
        if stack:
            print(f"❌ 错误: 以下标签未正确闭合: {stack}")
            return False
        
        print("✅ 所有标签嵌套正确")
        return True
    
    def validate_syntax(self) -> bool:
        """使用 ElementTree 验证XML语法"""
        print("\n" + "=" * 60)
        print("🔧 XML 语法验证")
        print("=" * 60)
        
        try:
            root = ET.fromstring(self.xml_string)
            print(f"✅ XML 语法有效")
            print(f"   根标签: <{root.tag}>")
            print(f"   子元素数量: {len(root)}")
            return True
        except ET.ParseError as e:
            print(f"❌ XML 语法错误: {e}")
            return False
    
    def get_tag_statistics(self) -> Dict:
        """获取标签统计信息"""
        stats = {
            'total': len(self.tags),
            'start_tags': 0,
            'end_tags': 0,
            'self_closing_tags': 0,
            'unique_tags': set()
        }
        
        for tag in self.tags:
            stats['unique_tags'].add(tag['name'])
            if tag['type'] == 'start':
                stats['start_tags'] += 1
            elif tag['type'] == 'end':
                stats['end_tags'] += 1
            else:
                stats['self_closing_tags'] += 1
        
        stats['unique_tags'] = list(stats['unique_tags'])
        return stats
    
    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_tag_statistics()
        
        print("\n" + "=" * 60)
        print("📊 标签统计")
        print("=" * 60)
        print(f"总标签数: {stats['total']}")
        print(f"开始标签: {stats['start_tags']}")
        print(f"结束标签: {stats['end_tags']}")
        print(f"自闭合标签: {stats['self_closing_tags']}")
        print(f"唯一标签数: {len(stats['unique_tags'])}")
        print(f"唯一标签: {', '.join(sorted(stats['unique_tags']))}")


def main():
    """主函数 - 演示XML标签识别与验证"""
    
    # 测试用例1: 有效的XML
    print("\n" + "🔵" * 30)
    print("测试用例 1: 有效的XML")
    print("🔵" * 30)
    
    xml_valid = """
    <person id="1" active="true">
        <name>张三</name>
        <age>25</age>
        <address>
            <city>北京</city>
            <street>长安街</street>
        </address>
        <hobbies>
            <hobby>阅读</hobby>
            <hobby>编程</hobby>
        </hobbies>
    </person>
    """
    
    validator1 = XMLTagValidator(xml_valid)
    validator1.print_all_tags()
    validator1.validate_nesting()
    validator1.validate_syntax()
    validator1.print_statistics()
    
    # 测试用例2: 标签不匹配的XML
    print("\n\n" + "🔴" * 30)
    print("测试用例 2: 标签不匹配的XML")
    print("🔴" * 30)
    
    xml_invalid = """
    <person>
        <name>李四</name>
        <age>30</age>
        <address>
            <city>上海</city>
        </person>  <!-- 错误: address 未闭合 -->
    """
    
    validator2 = XMLTagValidator(xml_invalid)
    validator2.print_all_tags()
    validator2.validate_nesting()
    validator2.validate_syntax()
    
    # 测试用例3: 包含自闭合标签的XML
    print("\n\n" + "🟢" * 30)
    print("测试用例 3: 包含自闭合标签的XML")
    print("🟢" * 30)
    
    xml_self_closing = """
    <config>
        <setting name="timeout" value="30"/>
        <setting name="debug" value="false"/>
        <database host="localhost" port="3306"/>
    </config>
    """
    
    validator3 = XMLTagValidator(xml_self_closing)
    validator3.print_all_tags()
    validator3.validate_nesting()
    validator3.validate_syntax()
    validator3.print_statistics()


if __name__ == "__main__":
    main()
