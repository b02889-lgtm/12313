# 测试工作流

## 概述

本文档定义了项目的测试流程，确保代码质量和功能稳定性。

## 测试类型

### 1. 单元测试

**目的**：验证单个函数、类或模块的功能

**要求**：
- 覆盖率目标：≥ 80%
- 测试独立运行
- 快速执行（< 1秒/测试）

**示例**：
```python
def test_calculate_sum():
    result = calculate_sum([1, 2, 3])
    assert result == 6
```

### 2. 集成测试

**目的**：验证多个组件协同工作

**要求**：
- 测试关键业务流程
- 使用测试数据库
- 模拟外部服务

**示例**：
```python
def test_user_registration_flow():
    # 创建用户
    user = create_user("test@example.com")
    # 验证邮件发送
    assert email_sent
    # 验证数据库记录
    assert user_in_database
```

### 3. 端到端测试

**目的**：模拟真实用户操作

**要求**：
- 测试主要用户场景
- 使用真实浏览器
- 定期执行

**示例**：
```javascript
test('用户登录流程', async () => {
  await page.goto('/login')
  await page.fill('#email', 'user@example.com')
  await page.fill('#password', 'password123')
  await page.click('#login-button')
  await expect(page).toHaveURL('/dashboard')
})
```

### 4. 性能测试

**目的**：验证系统性能指标

**指标**：
- 响应时间 < 200ms
- 并发用户数 ≥ 1000
- 错误率 < 0.1%

## 测试流程

### 1. 开发阶段

```bash
# 编写代码时同步编写测试
# 运行相关测试
npm test -- --watch

# 提交前运行完整测试套件
npm test
```

### 2. 代码审查

- [ ] 新功能包含测试
- [ ] 测试覆盖率达标
- [ ] 测试通过

### 3. 持续集成

```yaml
# CI 配置示例
test:
  script:
    - npm install
    - npm test
    - npm run test:coverage
  coverage: '/Code coverage: \d+\.\d+/'
```

## 测试工具

### JavaScript/TypeScript
- Jest - 单元测试框架
- Cypress - 端到端测试
- Supertest - API 测试

### Python
- pytest - 单元测试框架
- unittest - 标准库测试框架
- locust - 性能测试

### 通用工具
- Postman - API 测试
- JMeter - 性能测试
- Selenium - 浏览器自动化

## 测试最佳实践

1. **测试命名**
   - 使用描述性名称
   - 格式：`test_功能_场景_预期结果`

2. **测试隔离**
   - 每个测试独立运行
   - 不依赖测试执行顺序
   - 清理测试数据

3. **测试数据**
   - 使用固定测试数据
   - 避免随机数据
   - 覆盖边界情况

4. **断言清晰**
   - 使用明确的断言
   - 提供有意义的错误信息
   - 验证关键结果

## 测试报告

### 生成报告

```bash
# 生成覆盖率报告
npm run test:coverage

# 生成 HTML 报告
npm run test:report
```

### 报告内容

- 测试执行摘要
- 失败测试详情
- 代码覆盖率统计
- 性能指标

## 常见问题

### Q: 测试运行太慢怎么办？

A: 
- 使用测试并行执行
- 减少数据库操作
- 使用 mock 替代真实服务

### Q: 如何测试异步代码？

A:
- 使用 async/await
- 使用测试框架的异步支持
- 设置合理的超时时间

### Q: 测试环境如何配置？

A:
- 使用环境变量
- 创建测试配置文件
- 使用 Docker 容器化

## 注意事项

- 保持测试简单和可维护
- 定期更新测试用例
- 删除过时的测试
- 监控测试执行时间