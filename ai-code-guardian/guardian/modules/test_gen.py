"""
TestGen 模块 - AI 驱动的测试生成

自动为新增或修改的无测试函数生成 pytest 单元测试。
包含测试文件映射、LLM 测试生成和自动化验证。
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from guardian.core.ast_analyzer import ASTAnalyzer, FunctionInfo
from guardian.core.llm_client import LLMClient, LLMMessage


# ── 数据结构 ──────────────────────────────

@dataclass
class TestMapping:
    """源文件与测试文件的映射关系"""
    source_file: str
    test_file: str | None          # 对应的测试文件路径（可能不存在）
    test_file_exists: bool
    covered_functions: list[str]   # 已有测试覆盖的函数名
    uncovered_functions: list[str] # 未覆盖的函数名


@dataclass
class GeneratedTest:
    """LLM 生成的测试"""
    function_name: str
    test_code: str
    test_file_path: str
    is_valid: bool = False         # 语法是否有效
    run_passed: bool = False       # 运行是否通过
    error_message: str = ""


# ── T4.1 测试映射查找 ──────────────────────

class TestMapper:
    """测试文件映射器

    根据约定的命名规则，判断源文件是否有对应的测试文件，
    并分析测试覆盖情况。
    """

    # 常见的测试文件命名模式
    TEST_PATTERNS = [
        "test_{name}.py",           # test_utils.py
        "{name}_test.py",           # utils_test.py
        "tests/test_{name}.py",     # tests/test_utils.py
        "tests/{name}_test.py",     # tests/utils_test.py
    ]

    def __init__(self, repo_root: str | Path = ".") -> None:
        self.repo_root = Path(repo_root)
        self.analyzer = ASTAnalyzer()

    def find_test_file(self, source_file: str) -> str | None:
        """查找源文件对应的测试文件。

        Args:
            source_file: 源文件路径（相对于仓库根目录）。

        Returns:
            测试文件路径，不存在则返回 None。
        """
        source_path = Path(source_file)
        source_name = source_path.stem  # 如 "utils"
        source_dir = source_path.parent

        for pattern in self.TEST_PATTERNS:
            test_name = pattern.format(name=source_name)
            # 在源文件同目录下查找
            candidate = source_dir / test_name
            if (self.repo_root / candidate).is_file():
                return str(candidate)

            # 在仓库根目录下查找
            candidate = Path(test_name)
            if (self.repo_root / candidate).is_file():
                return str(candidate)

        return None

    def get_mapping(self, source_file: str, source_content: str) -> TestMapping:
        """获取源文件的完整测试映射信息。

        Args:
            source_file: 源文件路径。
            source_content: 源文件内容。

        Returns:
            TestMapping 实例。
        """
        test_file = self.find_test_file(source_file)
        test_exists = test_file is not None

        # 提取源文件中的公开函数
        source_funcs = self.analyzer.extract_public_api(source_content, source_file)
        source_func_names = [f.name for f in source_funcs]

        # 提取测试文件中已覆盖的函数
        covered = []
        if test_file and test_exists:
            test_path = self.repo_root / test_file
            if test_path.is_file():
                test_content = test_path.read_text(encoding="utf-8")
                covered = self._extract_covered_functions(test_content, source_func_names)

        uncovered = [f for f in source_func_names if f not in covered]

        # 如果没有测试文件，建议一个路径
        suggested_test_file = test_file
        if not test_file:
            source_name = Path(source_file).stem
            suggested_test_file = str(Path(source_file).parent / f"test_{source_name}.py")

        return TestMapping(
            source_file=source_file,
            test_file=suggested_test_file,
            test_file_exists=test_exists,
            covered_functions=covered,
            uncovered_functions=uncovered,
        )

    def _extract_covered_functions(
        self, test_content: str, source_func_names: list[str]
    ) -> list[str]:
        """从测试文件内容中提取已覆盖的源函数名。

        简单启发式：如果测试文件中存在 test_<func_name> 函数，
        则认为 <func_name> 已有测试覆盖。

        Args:
            test_content: 测试文件内容。
            source_func_names: 源文件中的函数名列表。

        Returns:
            已覆盖的函数名列表。
        """
        test_funcs = self.analyzer.extract_functions(test_content)
        test_func_names = {f.name for f in test_funcs}

        covered = []
        for func_name in source_func_names:
            # 检查各种测试命名约定
            possible_tests = [
                f"test_{func_name}",
                f"test_{func_name}_success",
                f"test_{func_name}_error",
                f"test_{func_name}_basic",
            ]
            if any(t in test_func_names for t in possible_tests):
                covered.append(func_name)

        return covered


# ── T4.2 测试生成 Prompt ──────────────────

TEST_GEN_SYSTEM_PROMPT = """你是一个专业的 Python 测试工程师。
你的任务是为给定的函数生成高质量的 pytest 单元测试。

规则：
1. 使用 pytest 框架和 unittest.mock
2. 测试函数命名：test_<function_name>_<scenario>
3. 每个函数至少生成 2-3 个测试用例（正常路径、边界、错误处理）
4. 使用 fixture 和参数化（@pytest.mark.parametrize）
5. 添加清晰的 docstring 说明每个测试的目的
6. 只输出可直接运行的 Python 代码"""

TEST_GEN_USER_TEMPLATE = """请为以下函数生成 pytest 单元测试。

源文件: {filepath}

需要测试的函数:
```python
{function_code}
```

现有的 import 和依赖:
```python
{imports}
```

请生成完整的测试文件代码（包含所有必要的 import）。"""


class TestGenerator:
    """LLM 驱动的测试生成器"""

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm = llm_client

    def generate_tests(
        self,
        functions: list[FunctionInfo],
        source_file: str,
        source_content: str,
    ) -> list[GeneratedTest]:
        """为函数列表生成测试。

        Args:
            functions: 需要生成测试的函数列表。
            source_file: 源文件路径。
            source_content: 源文件完整内容。

        Returns:
            GeneratedTest 列表。
        """
        if not functions:
            return []

        # 提取 import 语句
        imports = self._extract_imports(source_content)

        results = []
        for func in functions:
            test = self._generate_single_test(func, source_file, imports)
            results.append(test)

        return results

    def _generate_single_test(
        self,
        func: FunctionInfo,
        source_file: str,
        imports: str,
    ) -> GeneratedTest:
        """为单个函数生成测试。

        Args:
            func: 函数信息。
            source_file: 源文件路径。
            imports: import 语句。

        Returns:
            GeneratedTest 实例。
        """
        user_prompt = TEST_GEN_USER_TEMPLATE.format(
            filepath=source_file,
            function_code=func.body_source,
            imports=imports,
        )

        messages = [
            LLMMessage(role="system", content=TEST_GEN_SYSTEM_PROMPT),
            LLMMessage(role="user", content=user_prompt),
        ]

        test_file = str(Path(source_file).parent / f"test_{Path(source_file).stem}.py")

        try:
            response = self.llm.chat(messages, temperature=0.2, max_tokens=3000)
            test_code = self._extract_code_block(response.content)

            # 验证语法
            is_valid = self._validate_syntax(test_code)

            return GeneratedTest(
                function_name=func.name,
                test_code=test_code,
                test_file_path=test_file,
                is_valid=is_valid,
            )
        except Exception as e:
            return GeneratedTest(
                function_name=func.name,
                test_code="",
                test_file_path=test_file,
                is_valid=False,
                error_message=str(e),
            )

    def _extract_code_block(self, content: str) -> str:
        """从 LLM 响应中提取代码块。

        Args:
            content: LLM 响应内容。

        Returns:
            提取的代码字符串。
        """
        # 匹配 ```python ... ``` 代码块
        pattern = r"```python\s*\n(.*?)```"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0].strip()

        # 如果没有代码块标记，返回整个内容
        return content.strip()

    def _validate_syntax(self, code: str) -> bool:
        """验证 Python 代码语法。

        Args:
            code: Python 代码字符串。

        Returns:
            True 表示语法有效。
        """
        import ast as ast_module
        try:
            ast_module.parse(code)
            return True
        except SyntaxError:
            return False

    def _extract_imports(self, source: str) -> str:
        """从源文件中提取 import 语句。

        Args:
            source: 源文件内容。

        Returns:
            import 语句字符串。
        """
        lines = source.splitlines()
        import_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                import_lines.append(line)
        return "\n".join(import_lines)


# ── T4.3 自动化运行验证 ──────────────────

class TestRunner:
    """测试自动运行和验证"""

    def run_test(self, test_code: str, test_file: str, cwd: str = ".") -> tuple[bool, str]:
        """运行生成的测试代码。

        将代码写入临时文件，使用 pytest 运行，然后清理。

        Args:
            test_code: 测试代码。
            test_file: 测试文件路径。
            cwd: 工作目录。

        Returns:
            (是否通过, 输出信息) 元组。
        """
        import subprocess
        import tempfile

        # 写入临时文件
        tmp_path = Path(cwd) / f".guardian_tmp_{Path(test_file).name}"
        try:
            tmp_path.write_text(test_code, encoding="utf-8")

            result = subprocess.run(
                ["python", "-m", "pytest", str(tmp_path), "-v", "--tb=short"],
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )

            passed = result.returncode == 0
            output = result.stdout + result.stderr
            return passed, output

        except subprocess.TimeoutExpired:
            return False, "测试运行超时（30秒）"
        except Exception as e:
            return False, f"测试运行失败: {e}"
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


# ── T4.4 结果过滤 ──────────────────────

class TestFilter:
    """过滤和优化生成的测试结果"""

    def filter_results(
        self, tests: list[GeneratedTest], run_verification: bool = False, cwd: str = "."
    ) -> list[GeneratedTest]:
        """过滤生成的测试，移除无效结果。

        Args:
            tests: 生成的测试列表。
            run_verification: 是否运行验证。
            cwd: 工作目录。

        Returns:
            过滤后的有效测试列表。
        """
        runner = TestRunner() if run_verification else None
        valid_tests = []

        for test in tests:
            if not test.is_valid:
                continue

            if runner:
                passed, output = runner.run_test(test.test_code, test.test_file_path, cwd)
                test.run_passed = passed
                if not passed:
                    test.error_message = output

            valid_tests.append(test)

        return valid_tests
