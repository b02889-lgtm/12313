#!/usr/bin/env python3
"""
Test script to demonstrate skill functionality
This script shows how the skills would be used
"""

def test_calculator_skill():
    """Test calculator skill functionality"""
    print("=== Calculator Skill Test ===")
    print("User request: '帮我解方程 x^2 - 5x + 6 = 0'")
    print()
    
    # This is what the calculator skill would do:
    import math
    
    # Solve quadratic equation: x^2 - 5x + 6 = 0
    a, b, c = 1, -5, 6
    discriminant = b**2 - 4*a*c
    
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        print(f"Calculator Skill Response:")
        print(f"方程 x^2 - 5x + 6 = 0 的解为:")
        print(f"x1 = {x1}")
        print(f"x2 = {x2}")
    else:
        print("方程无实数解")
    
    print()

def test_chinese_poetry_skill():
    """Test chinese poetry skill functionality"""
    print("=== Chinese Poetry Skill Test ===")
    print("User request: '帮我写一首关于春天的七言绝句'")
    print()
    
    # This is what the chinese poetry skill would do:
    poem = """春风拂面醉桃花，
新燕归来绕树斜。
陌上青青杨柳绿，
满园生意属谁家。"""
    
    print("Chinese Poetry Skill Response:")
    print("为您创作一首关于春天的七言绝句：")
    print()
    print(poem)
    print()
    print("创作说明：")
    print("- 采用七言绝句格式，四句二十八字")
    print("- 押'麻'韵（花、斜、家）")
    print("- 描绘了春风吹拂、桃花盛开、燕子归来、杨柳青青的春日美景")
    print("- 表达了对春天生机勃勃的赞美之情")

def main():
    """Main test function"""
    print("Skill System Test")
    print("=" * 50)
    print()
    
    test_calculator_skill()
    test_chinese_poetry_skill()
    
    print("=" * 50)
    print("Test completed!")
    print()
    print("技能验证说明：")
    print("1. 两个技能功能完全不同，便于系统识别")
    print("2. calculator技能处理数学计算")
    print("3. chinese-poetry技能处理诗词创作")
    print("4. 系统应能根据用户请求内容自动选择相应技能")

if __name__ == "__main__":
    main()