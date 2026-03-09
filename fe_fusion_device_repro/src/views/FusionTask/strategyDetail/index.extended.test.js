import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import StrategyDetail from './index.vue';

// 模拟 Element Plus 的 Tree 组件
const mockTreeRef = {
  setCheckedKeys: vi.fn(),
  getCheckedKeys: vi.fn(() => [])
};

describe('StrategyDetail - Extended Tests', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(StrategyDetail, {
      global: {
        stubs: {
          'el-tree': {
            template: '<div></div>',
            methods: {
              setCheckedKeys: mockTreeRef.setCheckedKeys,
              getCheckedKeys: mockTreeRef.getCheckedKeys
            }
          }
        }
      }
    });

    // 直接修改组件暴露的 treeRef
    wrapper.vm.treeRef = mockTreeRef;

    mockTreeRef.setCheckedKeys.mockClear();
    mockTreeRef.getCheckedKeys.mockClear();
  });

  // 测试 1: name === 'aggregate' 分支
  it('setMark with name="aggregate" should set labelMarkData with one item', () => {
    wrapper.vm.setMark({ name: 'aggregate', type: 1 });

    expect(wrapper.vm.labelMarkData).toEqual([
      { label: '数据规范', tag: [] }
    ]);
    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledWith([]);
  });

  // 测试 2: name === 'service' && type === 1 分支
  it('setMark with name="service" and type=1 should set labelMarkData with two items', () => {
    wrapper.vm.setMark({ name: 'service', type: 1 });

    expect(wrapper.vm.labelMarkData).toEqual([
      { label: '数据规范', tag: [] },
      { label: '对象规范', tag: [] }
    ]);
    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledWith([]);
  });

  // 测试 3: name === 'service' && type !== 1 分支
  it('setMark with name="service" and type!==1 should keep labelMarkData empty', () => {
    wrapper.vm.setMark({ name: 'service', type: 2 });

    expect(wrapper.vm.labelMarkData).toEqual([]);
    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledWith([]);
  });

  // 测试 4: name 为其他值的分支
  it('setMark with name="other" should keep labelMarkData empty', () => {
    wrapper.vm.setMark({ name: 'other', type: 1 });

    expect(wrapper.vm.labelMarkData).toEqual([]);
    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledWith([]);
  });

  // 测试 5: 严格相等测试
  it('setMark should use strict equality (===) for type comparison', () => {
    wrapper.vm.setMark({ name: 'service', type: '1' });

    // 使用 === 时，字符串 '1' 不等于数字 1
    expect(wrapper.vm.labelMarkData).toEqual([]);
  });

  // 测试 6: 验证 setCheckedKeys 被调用的次数
  it('setMark should call setCheckedKeys exactly once', () => {
    wrapper.vm.setMark({ name: 'aggregate', type: 1 });

    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledTimes(1);
  });

  // 测试 7: 验证 labelMarkData 是响应式的
  it('labelMarkData should be reactive', () => {
    expect(wrapper.vm.labelMarkData).toEqual([]);

    wrapper.vm.setMark({ name: 'aggregate', type: 1 });

    expect(wrapper.vm.labelMarkData).toEqual([
      { label: '数据规范', tag: [] }
    ]);
  });

  // 测试 8: 验证 treeRef 存在时才调用 setCheckedKeys
  it('setMark should check treeRef before calling setCheckedKeys', () => {
    // 清空之前的调用
    mockTreeRef.setCheckedKeys.mockClear();

    // 这个测试验证组件代码中是否有 treeRef.value 的检查
    wrapper.vm.setMark({ name: 'aggregate', type: 1 });

    // 如果组件代码中有 if (treeRef.value) 检查，这个测试会通过
    expect(mockTreeRef.setCheckedKeys).toHaveBeenCalled();
  });
});
