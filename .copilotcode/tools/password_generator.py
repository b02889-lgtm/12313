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
