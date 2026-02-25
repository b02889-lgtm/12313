---
name: file-organizer
description: 文件整理助手技能。当用户需要以下功能时使用：(1) 按文件类型自动整理文件夹、(2) 批量重命名文件、(3) 查找并删除重复文件、(4) 按日期/大小等条件组织文件、(5) 清理空文件夹。本技能专注于文件系统管理和自动化整理任务。
---

# File Organizer

文件整理助手，帮助用户自动化管理和组织文件系统。

## 核心功能

### 1. 按类型整理文件

使用 `scripts/organize_by_type.py` 脚本按文件扩展名自动分类：

```bash
python scripts/organize_by_type.py <目标文件夹路径>
```

功能：
- 自动创建分类文件夹（图片、文档、视频、音频、压缩包、其他）
- 按文件扩展名移动文件到对应分类
- 保留原始文件，仅做移动操作

### 2. 批量重命名

使用 `scripts/batch_rename.py` 脚本批量重命名文件：

```bash
python scripts/batch_rename.py <文件夹路径> <命名模式>
```

示例：
```bash
python scripts/batch_rename.py ./photos "vacation_2024_{:03d}"
```

### 3. 查找重复文件

使用 `scripts/find_duplicates.py` 脚本查找重复文件：

```bash
python scripts/find_duplicates.py <文件夹路径>
```

输出重复文件列表，可选择删除或移动。

### 4. 清理空文件夹

使用 `scripts/remove_empty_folders.py` 脚本：

```bash
python scripts/remove_empty_folders.py <文件夹路径>
```

## 文件分类规则

| 分类 | 扩展名 |
|------|--------|
| 图片 | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp |
| 文档 | .pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx, .md |
| 视频 | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm |
| 音频 | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a |
| 压缩包 | .zip, .rar, .7z, .tar, .gz, .bz2 |
| 代码 | .py, .js, .html, .css, .java, .cpp, .c, .h, .json, .xml |
| 其他 | 其他所有扩展名 |

## 使用示例

**整理下载文件夹：**
```bash
python scripts/organize_by_type.py ~/Downloads
```

**整理当前文件夹：**
```bash
python scripts/organize_by_type.py .
```

**批量重命名照片：**
```bash
python scripts/batch_rename.py ./photos "IMG_{:04d}.jpg"
```

## 注意事项

1. 所有脚本在执行前会显示预览，确认后才执行
2. 操作前建议备份重要文件
3. 脚本不会覆盖已存在的文件
4. 支持递归处理子文件夹（可选参数）
