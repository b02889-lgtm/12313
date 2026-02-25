# 代码审查工作流

## 概述

本工作流用于指导完成代码审查任务，确保代码质量、可维护性和符合项目规范。

## 工作流步骤

### 1. 审查前准备

- [ ] 确认 Pull Request 或代码变更范围
- [ ] 阅读相关需求和设计文档
- [ ] 了解变更的业务背景
- [ ] 准备审查环境

### 2. 代码结构审查

- [ ] 检查文件组织结构是否合理
- [ ] 验证模块划分是否清晰
- [ ] 确认命名规范是否一致
- [ ] 检查代码长度和复杂度

```python
# 代码结构检查清单
# ✓ 文件命名遵循项目规范（snake_case 或 camelCase）
# ✓ 类名使用 PascalCase
# ✓ 函数名使用 snake_case
# ✓ 常量使用 UPPER_CASE
# ✓ 单个函数不超过 50 行
# ✓ 单个文件不超过 500 行
```

### 3. 代码质量审查

- [ ] 检查代码可读性
- [ ] 验证注释是否充分
- [ ] 确认没有重复代码
- [ ] 检查错误处理是否完善

```python
# 代码质量检查示例

# ✓ 好的代码示例
def calculate_discount(price: float, discount_rate: float) -> float:
    """
    计算折扣后的价格
    
    Args:
        price: 原始价格
        discount_rate: 折扣率（0-1之间）
    
    Returns:
        折扣后的价格
    
    Raises:
        ValueError: 当价格或折扣率无效时
    """
    if price < 0:
        raise ValueError("价格不能为负数")
    if not 0 <= discount_rate <= 1:
        raise ValueError("折扣率必须在0到1之间")
    
    return price * (1 - discount_rate)

# ✗ 需要改进的代码
def calc(p, d):
    return p * d
```

### 4. 功能正确性审查

- [ ] 验证业务逻辑是否正确
- [ ] 检查边界条件处理
- [ ] 确认异常情况处理
- [ ] 验证数据验证逻辑

```python
# 功能正确性检查点
# ✓ 输入验证
# ✓ 边界值处理（空值、最大值、最小值）
# ✓ 异常捕获和处理
# ✓ 业务规则实现
# ✓ 数据一致性保证
```

### 5. 性能审查

- [ ] 检查是否有性能瓶颈
- [ ] 验证数据库查询效率
- [ ] 确认内存使用是否合理
- [ ] 检查是否有不必要的计算

```python
# 性能优化检查

# ✓ 使用列表推导式代替循环
result = [x * 2 for x in data]  # 好
# result = []
# for x in data:
#     result.append(x * 2)  # 较慢

# ✓ 使用生成器处理大数据
def process_large_data(data):
    for item in data:
        yield process_item(item)

# ✓ 避免在循环中重复计算
total = sum(data)  # 在循环外计算
for item in data:
    ratio = item / total  # 使用预计算的值
```

### 6. 安全性审查

- [ ] 检查输入验证和过滤
- [ ] 验证敏感数据处理
- [ ] 确认权限检查
- [ ] 检查 SQL 注入风险

```python
# 安全性检查清单
# ✓ 所有用户输入都经过验证
# ✓ 敏感数据不记录在日志中
# ✓ 使用参数化查询防止 SQL 注入
# ✓ 敏感操作需要权限验证
# ✓ 密码和密钥不硬编码
```

### 7. 测试覆盖审查

- [ ] 检查单元测试是否充分
- [ ] 验证测试用例覆盖主要场景
- [ ] 确认边界条件有测试
- [ ] 检查测试是否可维护

```python
# 测试覆盖检查
# ✓ 每个公共函数都有测试
# ✓ 正常流程有测试
# ✓ 异常情况有测试
# ✓ 边界值有测试
# ✓ 测试命名清晰描述测试内容

import unittest

class TestCalculator(unittest.TestCase):
    def test_calculate_discount_normal(self):
        """测试正常折扣计算"""
        result = calculate_discount(100, 0.2)
        self.assertEqual(result, 80)
    
    def test_calculate_discount_invalid_price(self):
        """测试无效价格"""
        with self.assertRaises(ValueError):
            calculate_discount(-100, 0.2)
```

### 8. 文档审查

- [ ] 检查函数和类的文档字符串
- [ ] 验证 README 是否更新
- [ ] 确认 API 文档是否同步
- [ ] 检查注释是否准确

```python
# 文档检查清单
# ✓ 所有公共函数有 docstring
# ✓ 复杂逻辑有行内注释
# ✓ README 包含使用说明
# ✓ 变更日志已更新
# ✓ API 文档已同步
```

### 9. 审查反馈

- [ ] 提供建设性的反馈意见
- [ ] 指出具体问题和改进建议
- [ ] 给出代码示例（如适用）
- [ ] 标记问题的优先级

```markdown
# 审查反馈模板

## 总体评价
[代码质量总体评价]

## 主要问题
### 🔴 高优先级
- [问题描述]
  - 位置：[文件名:行号]
  - 建议：[改进建议]
  - 示例：[代码示例]

### 🟡 中优先级
- [问题描述]
  - 位置：[文件名:行号]
  - 建议：[改进建议]

### 🟢 低优先级
- [问题描述]
  - 位置：[文件名:行号]
  - 建议：[改进建议]

## 优点
- [列出代码的优点]

## 其他建议
- [其他改进建议]
```

### 10. 审查后跟进

- [ ] 确认开发者已处理反馈
- [ ] 验证修改是否解决问题
- [ ] 检查是否引入新问题
- [ ] 批准或要求进一步修改

## 审查检查清单

### 代码规范
- [ ] 遵循项目代码风格指南
- [ ] 使用一致的命名约定
- [ ] 适当的代码格式化
- [ ] 合理的代码缩进和空行

### 功能实现
- [ ] 实现符合需求
- [ ] 逻辑正确无误
- [ ] 边界条件处理
- [ ] 错误处理完善

### 代码质量
- [ ] 代码可读性好
- [ ] 注释清晰准确
- [ ] 无重复代码
- [ ] 模块化设计合理

### 测试
- [ ] 测试覆盖充分
- [ ] 测试用例有效
- [ ] 测试通过
- [ ] 测试可维护

### 文档
- [ ] 代码文档完整
- [ ] API 文档更新
- [ ] README 更新
- [ ] 变更日志记录

## 常用命令

```bash
# 查看代码变更
git diff main..feature-branch

# 查看文件统计
git diff --stat main..feature-branch

# 运行测试
pytest tests/

# 代码格式检查
black --check .
flake8 .
```

## 注意事项

- 保持客观和建设性的态度
- 关注代码质量而非个人风格
- 提供具体的改进建议
- 及时响应审查请求
- 尊重开发者的工作

## 审查工具推荐

- **静态代码分析**: pylint, flake8, ESLint
- **代码格式化**: black, prettier
- **安全扫描**: bandit, Snyk
- **测试覆盖率**: coverage.py, pytest-cov
- **代码审查平台**: GitHub PR, GitLab MR, Phabricator
