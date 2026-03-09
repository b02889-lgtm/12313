# 新的单元测试计划

## 目标
为 `setMark` 方法设计更全面的测试用例，覆盖所有分支逻辑，确保组件在各种输入条件下都能正确工作。

## 测试用例设计

### 1. 测试 `name === 'aggregate'` 分支
- **输入**: `{ name: 'aggregate', type: 1 }`
- **预期结果**:
  - `labelMarkData.value` 应该被设置为包含一个对象的数组，该对象的 `label` 为 '数据规范'，`tag` 为空数组。
  - `treeRef.value.setCheckedKeys([])` 应该被调用一次。

### 2. 测试 `name === 'service' && type === 1` 分支
- **输入**: `{ name: 'service', type: 1 }`
- **预期结果**:
  - `labelMarkData.value` 应该被设置为包含两个对象的数组，第一个对象的 `label` 为 '数据规范'，第二个对象的 `label` 为 '对象规范'，两个对象的 `tag` 都为空数组。
  - `treeRef.value.setCheckedKeys([])` 应该被调用一次。

### 3. 测试 `name === 'service' && type !== 1` 分支
- **输入**: `{ name: 'service', type: 2 }`
- **预期结果**:
  - `labelMarkData.value` 应该保持不变（或被设置为空数组，取决于具体实现）。
  - `treeRef.value.setCheckedKeys([])` 应该被调用一次。

### 4. 测试未覆盖的 `name` 分支
- **输入**: `{ name: 'other', type: 1 }`
- **预期结果**:
  - `labelMarkData.value` 应该保持不变（或被设置为空数组，取决于具体实现）。
  - `treeRef.value.setCheckedKeys([])` 应该被调用一次。

## 实现步骤
1. ~~在 `index.test.js` 中添加新的测试用例。~~ [已完成]
2. 运行测试，确保所有新添加的测试用例都能通过。
3. 根据测试结果调整组件代码或测试用例，直到所有测试都通过。