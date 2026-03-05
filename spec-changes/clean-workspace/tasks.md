# 任务清单：整理工作区文件结构（clean-workspace）

## 阶段 0：回滚保障

- [ ] **0.1** 执行 `git add -A && git commit -m "备份：整理前的工作区快照"` 创建回滚点
- [ ] **0.2** 记录 commit hash，以备需要 `git reset --hard <hash>` 回退

## 阶段 1：准备工作

- [x] **1.1** 检查 Python 文件之间的 import 依赖关系 ✅ 已完成
  - 发现 3 个跨文件依赖：
    - `file_utils_examples.py` → `from file_utils import FileUtils`
    - `test_demo.py` → `from demo import Calculator`
    - `test_weather_mcp.py` → `sys.path.insert(0, 'weather-mcp-server')`
  - `data_processor.py` 无被引用，可安全移动
- [ ] **1.2** 检查批处理脚本（`.bat`、`.vbs`）中的硬编码路径
- [ ] **1.3** 检查 JSON 配置文件中是否引用了根目录下的文件

## 阶段 2：创建目录结构

- [ ] **2.1** 创建 `scripts/` 目录
- [ ] **2.2** 创建 `demos/` 目录
- [ ] **2.3** 创建 `data-analysis/` 目录
- [ ] **2.4** 创建 `tests/` 目录
- [ ] **2.5** 创建 `docs/` 和 `docs/mcp/` 目录
- [ ] **2.6** 创建 `mcp-config/` 目录
- [ ] **2.7** 创建 `figma/` 目录
- [ ] **2.8** 创建 `archive/` 目录

## 阶段 3：移动文件

按类别分批移动，每批移动后验证：

- [ ] **3.1** 移动实用工具脚本到 `scripts/`
  - `get_current_time.py`、`get_current_time.js`、`get_current_time.ps1`
  - `add_python_to_path.ps1`、`file_utils.py`、`file_batch_processor.py`
  - `data_processor.py`、`random_data_generator.py`、`xml_tag_validator.py`、`npm_docs_tool.py`

- [ ] **3.2** 移动演示代码到 `demos/`
  - `hello_world.py`、`simple_addition.py`、`simple_demo.py`、`demo.py`
  - `example_code.py`、`example_script.py`、`new_example.py`、`my_new_code.py`
  - `advanced_math_demo.py`、`calculator.py`、`check_equality.py`
  - `file_utils_examples.py`
  - ⚠️ `test_demo.py` 不再归入此处，已移至 3.4（tests）

- [ ] **3.3** 移动数据分析文件到 `data-analysis/`
  - `analyze_sample_data.py`、`data_analysis.py`、`data_analysis_demo.py`
  - `data_analysis_report.py`、`data_analysis_simple.py`
  - `sample_data.csv`、`sample_data.json`、`analysis_result.csv`

- [ ] **3.4** 移动测试文件到 `tests/`
  - `test_demo.py`（从根目录，非 demos/）
  - `test_calculator_skill.py`、`test_skills.py`
  - `test_weather_api.py`、`test_weather_mcp.py`

- [ ] **3.5** 移动文档到 `docs/` 和 `docs/mcp/`
  - 通用文档：`code_review_report.md`、`data_analysis_report_final.md`、`poetry_creation.md` 等
  - MCP 文档：`MCP服务诊断指南.md`、`MCP修复说明.md`、`figma-mcp-setup.md` 等

- [ ] **3.6** 移动 MCP 配置/修复脚本到 `mcp-config/`
  - `converted_mcp.json`、`mcp_settings_fixed.json`
  - `fix_mcp_config.py`、`fix_figma_mcp.py`、`mcp_stream_fix.py`
  - `update_figma_key.py`、`verify_mcp_config.py`

- [ ] **3.7** 移动 Figma 相关文件到 `figma/`
  - `start_figma_mcp.bat`、`start_figma_mcp_background.bat`
  - `start_figma_mcp_service.vbs`、`stop_figma_mcp.bat`
  - `figma_images/` → `figma/images/`

- [ ] **3.8** 移动临时/杂项文件到 `archive/`
  - `0KvaHMT.docx`、`请选择文件类型.txt`、`文件类型选择.txt`
  - `新建 文本文档.txt`、`新建文本文件.txt`
  - `new_file.txt`、`notes.txt`、`temp_delete_test.txt`

## 阶段 4：修复引用

根据 design.md 中的「Import 修复方案评估」，采用 sys.path.insert() 短期方案：

- [ ] **4.1** 修复 `demos/file_utils_examples.py` 中的 import
  - 原：`from file_utils import FileUtils`
  - 改：添加跨目录 import 修复代码块（见 design.md 模板）
- [ ] **4.2** 修复 `tests/test_demo.py` 中的 import
  - 原：`from demo import Calculator`
  - 改：添加 sys.path 修复，指向 `../demos`
- [ ] **4.3** 修复 `tests/test_weather_mcp.py` 中的路径
  - 原：`sys.path.insert(0, 'weather-mcp-server')`
  - 改：使用 `os.path.dirname(__file__)` 构建相对路径
- [ ] **4.4** 更新批处理脚本中的路径引用（如有）
- [ ] **4.5** 更新 README.md 中的文件引用（如有）

## 阶段 5：验证与清理

- [ ] **5.1** 验证移动后的文件结构是否符合 design.md 中的目标
- [ ] **5.2** 确认根目录只剩下预期的顶层文件（≤ 5 个）
- [ ] **5.3** 与用户确认 `archive/` 中的文件是否可以安全删除
- [ ] **5.4** 更新 README.md 说明新的目录结构
- [ ] **5.5** Git commit 整理结果

### 5.A 验收可视化对比（新增）

- [ ] **5.A.1** 生成「整理前」目录快照
  - 在开始前执行 `tree /F > before_cleanup.txt`（Windows）
  - 或使用 `ls -la > before_cleanup.txt`（Unix）
  - 保存到 `spec-changes/clean-workspace/before_cleanup.txt`

- [ ] **5.A.2** 生成「整理后」目录快照
  - 执行相同命令保存为 `after_cleanup.txt`
  - 保存到 `spec-changes/clean-workspace/after_cleanup.txt`

- [ ] **5.A.3** 生成对比报告
  - 创建 `spec-changes/clean-workspace/completion_report.md`，包含：
    ```markdown
    # 工作区整理完成报告
    
    ## 统计对比
    | 指标 | 整理前 | 整理后 |
    |------|--------|--------|
    | 根目录文件数 | XX | XX |
    | 目录数 | XX | XX |
    | archive/ 文件数 | - | XX |
    
    ## 移动的文件清单
    （列出每个文件的原位置 → 新位置）
    
    ## 修复的 import 关系
    （列出修改的文件和修改内容）
    
    ## 待用户确认事项
    - archive/ 中的 XX 个文件是否可删除
    ```

## 阶段 6：建立维护机制（新增）

防止未来混乱，参考 design.md 第 8 节「防止未来混乱的维护机制」

- [ ] **6.1** 更新 README.md，添加「文件组织指南」章节
  - 包含文件分类表格
  - 添加「请勿在根目录创建新文件」警告

- [ ] **6.2** 更新 .gitignore，添加根目录保护规则
  - 添加 `/*.txt`、`/*.docx`、`/temp_*`、`/新建*` 规则
  - 目的：阻止常见临时文件进入版本控制

- [ ] **6.3** 创建 archive/CLEANUP_LOG.md
  - 初始化清理记录文件
  - 记录首次整理的归档文件清单

- [ ] **6.4** 创建 scripts/workspace_health_check.py（可选）
  - 实现自动化健康检查脚本
  - 检查：根目录文件数、archive 大小、文件放置位置

- [ ] **6.5** 设置 pre-commit hook（可选）
  - 创建 .pre-commit-config.yaml
  - 配置自动检查根目录清洁度

---

**预计工作量**：中等（主要是文件移动，关键在于依赖检查和维护机制建立）
**建议执行方式**：按阶段顺序执行，每个阶段完成后确认无误再继续
**新增重点**：阶段 5.A 的可视化对比可帮助验证整理效果，阶段 6 确保长期维护
