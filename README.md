# Markdown 使用指南

这是一个示例 Markdown 文件。

## 什么是 Markdown？

Markdown 是一种轻量级标记语言，它允许人们使用易读易写的纯文本格式编写文档。

## 基本语法示例

### 文本格式

- **粗体文本**
- *斜体文本*
- ~~删除线~~

### 列表

1. 有序列表项 1
2. 有序列表项 2
3. 有序列表项 3

- 无序列表项
- 无序列表项
- 无序列表项

### 代码

行内代码：`console.log("你好世界")`

代码块：

```javascript
function greet(name) {
    console.log(`你好, ${name}！`);
}
```

### 链接和图片

[访问 GitHub](https://github.com)

### 表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |

---

## 新增章节（Architect 模式测试）

这个章节是在 **Architect 模式**下添加的，用于验证 Architect 模式是否能够正常编辑 Markdown 文件，而不会被错误地切换到 Code 模式。

### 验证要点

- [ ] Architect 模式可以直接编辑 `.md` 文件
- [ ] 不会触发 FileRestrictionError
- [ ] 不会自动切换到 Code 模式

---

*创建时间：2026-01-26*
*更新时间：2026-01-26（Code 模式 - 演示 search/replace）*

## 最新更新

- 添加了项目功能说明
- 更新了文档结构