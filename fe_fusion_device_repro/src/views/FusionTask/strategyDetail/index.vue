<template>
  <div>
    <!-- 假设有一个 Element Plus 的 Tree 组件，ref="treeRef" -->
    <el-tree ref="treeRef" :data="[]" node-key="id" />
    <button @click="setMark({ name: 'service', type: 1 })">Set Mark</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const treeRef = ref(null);
const labelMarkData = ref([]);

const setMark = (value) => {
  const { name, type } = value;
  
  // 截图中的部分代码
  if (name === 'aggregate') {
    labelMarkData.value = [
      {
        label: '数据规范',
        tag: []
      }
    ];
  } else if (name === 'service') { // 截图中的警告点 `==` -> `===`
    if (type === 1) {
      labelMarkData.value = [
        {
          label: '数据规范',
          tag: []
        },
        {
          label: '对象规范',
          tag: []
        }
      ];
    }
  }

  // 根据测试报错 `expect(mockTreeRef.setCheckedKeys).toHaveBeenCalledWith([])` 推测
  // 这里在 setMark 中，应该会去清除树的选中状态
  if (treeRef.value) {
    treeRef.value.setCheckedKeys([]);
  }
};

// 暴露出去以便测试
defineExpose({
  setMark,
  labelMarkData,
  treeRef
});
</script>
