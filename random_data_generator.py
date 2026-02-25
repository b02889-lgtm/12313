import random
import string

class RandomDataGenerator:
    """随机测试数据生成器"""
    
    # 常见中文姓氏
    SURNAMES = [
        '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
        '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
        '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
        '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕'
    ]
    
    # 常见中文名字用字
    GIVEN_NAMES = [
        '伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
        '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
        '平', '刚', '桂英', '玉兰', '萍', '毅', '浩', '宇', '轩', '涵',
        '梓', '子', '雨', '欣', '怡', '梦', '婷', '雪', '琳', '慧'
    ]
    
    # 常见邮箱域名
    EMAIL_DOMAINS = [
        'qq.com', '163.com', 'gmail.com', 'outlook.com', 
        'hotmail.com', '126.com', 'sina.com', 'yahoo.com'
    ]
    
    # 中国手机号段
    PHONE_PREFIXES = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '150', '151', '152', '153', '155', '156', '157', '158', '159',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189'
    ]
    
    # 常见城市
    CITIES = [
        '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都',
        '重庆', '西安', '苏州', '天津', '长沙', '郑州', '青岛', '大连',
        '厦门', '宁波', '无锡', '福州', '济南', '昆明', '合肥', '哈尔滨'
    ]
    
    # 常见街道
    STREETS = [
        '人民路', '建设路', '解放路', '和平路', '中山路', '文化路',
        '胜利路', '光明路', '新华路', '东风路', '红旗路', '朝阳路'
    ]
    
    @classmethod
    def generate_name(cls, length=None):
        """
        生成随机中文姓名
        
        参数:
            length (int): 姓名总长度，默认随机2或3
        
        返回:
            str: 随机中文姓名
        """
        if length is None:
            length = random.choice([2, 3])
            
        surname = random.choice(cls.SURNAMES)
        # 名的字数 = 总长度 - 1
        given_name_count = length - 1
        # 确保至少有1个字的名
        if given_name_count < 1: given_name_count = 1
        
        given_name = ''.join(random.choices(cls.GIVEN_NAMES, k=given_name_count))
        return surname + given_name
    
    @classmethod
    def generate_phone(cls):
        """
        生成随机手机号码
        
        返回:
            str: 11位随机手机号
        """
        prefix = random.choice(cls.PHONE_PREFIXES)
        suffix = ''.join(random.choices(string.digits, k=8))
        return prefix + suffix
    
    @classmethod
    def generate_email(cls, name=None):
        """
        生成随机邮箱地址
        
        参数:
            name (str): 可选，指定邮箱前缀（中文会被转换为随机字符）
        
        返回:
            str: 随机邮箱地址
        """
        prefix = ""
        # 如果提供了英文名，可以使用；如果是中文，我们通常需要拼音库，
        # 为了保持脚本零依赖，这里简单地忽略中文字符，改用随机字符
        if name:
            # 提取ASCII字符
            ascii_name = ''.join([c for c in name if c.isascii() and c.isalnum()])
            if ascii_name:
                prefix = ascii_name.lower()
        
        if not prefix:
            # 生成6-10位的随机字母数字组合
            chars = string.ascii_lowercase + string.digits
            prefix = ''.join(random.choices(chars, k=random.randint(6, 10)))
        
        domain = random.choice(cls.EMAIL_DOMAINS)
        return f"{prefix}@{domain}"
    
    @classmethod
    def generate_address(cls):
        """
        生成随机地址
        
        返回:
            str: 随机地址
        """
        city = random.choice(cls.CITIES)
        street = random.choice(cls.STREETS)
        number = random.randint(1, 999)
        return f"{city}{street}{number}号"
    
    @classmethod
    def generate_id_card(cls):
        """
        生成随机身份证号（18位，仅用于测试）
        
        返回:
            str: 18位身份证号
        """
        # 地区码（前6位）
        area_code = ''.join(random.choices(string.digits, k=6))
        # 出生日期（8位）
        year = random.randint(1970, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth_date = f"{year}{month:02d}{day:02d}"
        # 顺序码（3位）
        sequence = ''.join(random.choices(string.digits, k=3))
        # 校验码（1位）
        check_code = random.choice('0123456789X')
        
        return area_code + birth_date + sequence + check_code
    
    @classmethod
    def generate_user_profile(cls):
        """
        生成完整的用户资料
        
        返回:
            dict: 包含姓名、电话、邮箱、地址、身份证的用户资料
        """
        name = cls.generate_name()
        return {
            'name': name,
            'phone': cls.generate_phone(),
            'email': cls.generate_email(name),
            'address': cls.generate_address(),
            'id_card': cls.generate_id_card()
        }

def main():
    """主函数：演示各种随机数据生成"""
    print("=" * 50)
    print("随机测试数据生成器")
    print("=" * 50)
    
    # 生成单个数据
    print("\n【单个数据示例】")
    print(f"姓名: {RandomDataGenerator.generate_name()}")
    print(f"电话: {RandomDataGenerator.generate_phone()}")
    print(f"邮箱: {RandomDataGenerator.generate_email()}")
    print(f"地址: {RandomDataGenerator.generate_address()}")
    print(f"身份证: {RandomDataGenerator.generate_id_card()}")
    
    # 生成完整用户资料
    print("\n【完整用户资料】")
    profile = RandomDataGenerator.generate_user_profile()
    for key, value in profile.items():
        print(f"{key}: {value}")
    
    # 批量生成
    print("\n【批量生成5条用户数据】")
    for i in range(1, 6):
        profile = RandomDataGenerator.generate_user_profile()
        print(f"\n用户 {i}:")
        print(f"  姓名: {profile['name']}")
        print(f"  电话: {profile['phone']}")
        print(f"  邮箱: {profile['email']}")

if __name__ == "__main__":
    main()
