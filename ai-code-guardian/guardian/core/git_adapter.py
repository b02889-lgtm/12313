"""
Git 适配器模块

封装与 Git 仓库的交互操作，提供获取暂存区文件列表、
文件 HEAD 版本内容和 Staged 版本内容的能力。
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(Exception):
    """Git 操作相关错误"""
    pass


class GitAdapter:
    """Git 仓库适配器

    提供对 Git 暂存区（staged）文件的操作接口。
    使用 subprocess 调用 git 命令行工具。
    """

    def __init__(self, repo_path: str | Path | None = None) -> None:
        """初始化 Git 适配器。

        Args:
            repo_path: Git 仓库根目录路径。默认为当前工作目录。
        """
        self.repo_path = Path(repo_path).resolve() if repo_path else Path.cwd().resolve()
        self._validate_git_repo()

    def _validate_git_repo(self) -> None:
        """验证当前路径是否为有效的 Git 仓库。"""
        try:
            self._run_git("rev-parse", "--git-dir")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise GitError(
                f"'{self.repo_path}' 不是有效的 Git 仓库。请确保在 Git 仓库中运行 Guardian。"
            ) from e

    def _run_git(self, *args: str) -> str:
        """执行 git 命令并返回标准输出。

        Args:
            *args: git 命令参数（不包括 'git' 本身）。

        Returns:
            命令标准输出字符串（已 strip）。

        Raises:
            subprocess.CalledProcessError: 命令执行失败。
        """
        result = subprocess.run(
            ["git", *args],
            cwd=str(self.repo_path),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout.strip()

    def get_staged_files(self, extensions: tuple[str, ...] = (".py",)) -> list[str]:
        """获取暂存区中已修改的文件列表。

        仅返回指定扩展名的文件（默认为 .py）。
        包括新增 (A)、复制 (C)、修改 (M) 的文件。

        Args:
            extensions: 要过滤的文件扩展名元组。

        Returns:
            相对于仓库根目录的文件路径列表。
        """
        try:
            output = self._run_git(
                "diff", "--cached", "--name-only", "--diff-filter=ACM"
            )
        except subprocess.CalledProcessError:
            return []

        if not output:
            return []

        files = output.split("\n")
        return [f for f in files if any(f.endswith(ext) for ext in extensions)]

    def get_file_at_head(self, filepath: str) -> str | None:
        """获取文件在 HEAD 版本（最新提交）的内容。

        Args:
            filepath: 相对于仓库根目录的文件路径。

        Returns:
            文件内容字符串。如果文件在 HEAD 中不存在（如新文件），返回 None。
        """
        try:
            return self._run_git("show", f"HEAD:{filepath}")
        except subprocess.CalledProcessError:
            # 文件可能是新增的，HEAD 中不存在
            return None

    def get_staged_content(self, filepath: str) -> str:
        """获取文件在暂存区（staged/index）的内容。

        Args:
            filepath: 相对于仓库根目录的文件路径。

        Returns:
            文件内容字符串。

        Raises:
            GitError: 无法获取暂存区内容。
        """
        try:
            return self._run_git("show", f":{filepath}")
        except subprocess.CalledProcessError as e:
            raise GitError(
                f"无法获取文件 '{filepath}' 的暂存区内容: {e.stderr}"
            ) from e

    def get_diff_for_file(self, filepath: str) -> str:
        """获取文件在暂存区的 diff 输出。

        Args:
            filepath: 相对于仓库根目录的文件路径。

        Returns:
            diff 字符串。
        """
        try:
            return self._run_git("diff", "--cached", "--", filepath)
        except subprocess.CalledProcessError:
            return ""

    def get_repo_root(self) -> Path:
        """获取 Git 仓库根目录路径。

        Returns:
            仓库根目录的 Path 对象。
        """
        root = self._run_git("rev-parse", "--show-toplevel")
        return Path(root)

    def has_staged_changes(self) -> bool:
        """检查暂存区是否有变更。

        Returns:
            True 表示暂存区有变更。
        """
        try:
            output = self._run_git("diff", "--cached", "--name-only")
            return bool(output)
        except subprocess.CalledProcessError:
            return False
