import random
import string

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    """
    生成随机密码
    
    参数:
        length (int): 密码长度，默认16
        use_uppercase (bool): 是否使用大写字母
        use_lowercase (bool): 是否使用小写字母
        use_digits (bool): 是否使用数字
        use_symbols (bool): 是否使用特殊符号
    
    返回:
        str: 生成的随机密码
    """
    chars = ''
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += '!@#$%^&*()-_=+[]{}|;:,.<>?'
    
    if not chars:
        raise ValueError("至少需要选择一种字符类型")
    
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == '__main__':
    print("=" * 50)
    print("密码生成器演示")
    print("=" * 50)

    # 1. 默认配置（16位，包含所有字符类型）
    pwd1 = generate_password()
    print(f"\n1. 默认配置（16位，含大小写+数字+符号）:")
    print(f"   {pwd1}")

    # 2. 纯数字密码（6位PIN码）
    pwd2 = generate_password(length=6, use_uppercase=False, use_lowercase=False, use_digits=True, use_symbols=False)
    print(f"\n2. 6位 PIN 码（纯数字）:")
    print(f"   {pwd2}")

    # 3. 仅字母+数字（12位，无特殊符号）
    pwd3 = generate_password(length=12, use_symbols=False)
    print(f"\n3. 12位字母+数字（无特殊符号）:")
    print(f"   {pwd3}")

    # 4. 高强度密码（32位）
    pwd4 = generate_password(length=32)
    print(f"\n4. 32位高强度密码:")
    print(f"   {pwd4}")

    # 5. 批量生成5个密码
    print(f"\n5. 批量生成5个20位密码:")
    for i in range(5):
        print(f"   [{i+1}] {generate_password(length=20)}")

    print("\n" + "=" * 50)
    print("密码生成完成！")
