"""
API Diff 对比引擎

比较旧版本(HEAD)和新版本(Staged)的公开 API 签名，
检测新增、删除和修改的 API，并进行破坏性分级。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from guardian.core.ast_analyzer import ASTAnalyzer, APISignature, ParameterInfo


class ChangeLevel(str, Enum):
    """API 变更的严重程度分级"""
    SAFE = "SAFE"          # 安全变更：新增方法、新增可选参数
    WARNING = "WARNING"    # 警告：重命名参数、改变默认值
    BREAKING = "BREAKING"  # 破坏性：删除参数、删除方法、改变返回类型


@dataclass
class ParameterChange:
    """参数级别的变更记录"""
    param_name: str
    change_type: str       # "added" / "removed" / "type_changed" / "default_changed" / "renamed"
    old_value: str | None = None
    new_value: str | None = None
    level: ChangeLevel = ChangeLevel.SAFE


@dataclass
class APIChange:
    """单个 API 的变更记录"""
    qualified_name: str
    change_type: str       # "added" / "removed" / "modified"
    level: ChangeLevel
    file_path: str
    line: int
    details: list[ParameterChange] = field(default_factory=list)
    old_signature: APISignature | None = None
    new_signature: APISignature | None = None

    @property
    def summary(self) -> str:
        """生成变更摘要描述"""
        if self.change_type == "added":
            return f"✅ 新增 API: {self.qualified_name}"
        elif self.change_type == "removed":
            return f"❌ 删除 API: {self.qualified_name}"
        else:
            detail_strs = [f"  - {d.change_type}: {d.param_name}" for d in self.details]
            return f"⚠️ 修改 API: {self.qualified_name}\n" + "\n".join(detail_strs)


@dataclass
class DiffReport:
    """完整的 API Diff 报告"""
    file_path: str
    changes: list[APIChange] = field(default_factory=list)

    @property
    def has_breaking(self) -> bool:
        return any(c.level == ChangeLevel.BREAKING for c in self.changes)

    @property
    def has_warnings(self) -> bool:
        return any(c.level == ChangeLevel.WARNING for c in self.changes)

    @property
    def max_level(self) -> ChangeLevel:
        if self.has_breaking:
            return ChangeLevel.BREAKING
        if self.has_warnings:
            return ChangeLevel.WARNING
        return ChangeLevel.SAFE

    @property
    def stats(self) -> dict[str, int]:
        return {
            "added": sum(1 for c in self.changes if c.change_type == "added"),
            "removed": sum(1 for c in self.changes if c.change_type == "removed"),
            "modified": sum(1 for c in self.changes if c.change_type == "modified"),
            "breaking": sum(1 for c in self.changes if c.level == ChangeLevel.BREAKING),
            "warning": sum(1 for c in self.changes if c.level == ChangeLevel.WARNING),
            "safe": sum(1 for c in self.changes if c.level == ChangeLevel.SAFE),
        }


class APIDiffEngine:
    """API 对比引擎

    使用 ASTAnalyzer 提取新旧版本的结构化 API 签名，
    然后逐项对比参数变化，生成带分级的变更报告。
    """

    def __init__(self) -> None:
        self.analyzer = ASTAnalyzer()

    def compare(
        self,
        old_source: str | None,
        new_source: str,
        filepath: str = "<unknown>",
    ) -> DiffReport:
        """对比新旧源码的公开 API 签名。

        Args:
            old_source: 旧版本源码（HEAD）。None 表示新文件。
            new_source: 新版本源码（Staged）。
            filepath: 文件路径。

        Returns:
            DiffReport 变更报告。
        """
        report = DiffReport(file_path=filepath)

        # 提取结构化签名
        old_sigs = {}
        if old_source:
            for sig in self.analyzer.extract_api_signatures(old_source, filepath):
                old_sigs[sig.qualified_name] = sig

        new_sigs = {}
        for sig in self.analyzer.extract_api_signatures(new_source, filepath):
            new_sigs[sig.qualified_name] = sig

        old_names = set(old_sigs.keys())
        new_names = set(new_sigs.keys())

        # 新增的 API
        for name in sorted(new_names - old_names):
            sig = new_sigs[name]
            report.changes.append(APIChange(
                qualified_name=name,
                change_type="added",
                level=ChangeLevel.SAFE,
                file_path=filepath,
                line=sig.line_start,
                new_signature=sig,
            ))

        # 删除的 API
        for name in sorted(old_names - new_names):
            sig = old_sigs[name]
            report.changes.append(APIChange(
                qualified_name=name,
                change_type="removed",
                level=ChangeLevel.BREAKING,
                file_path=filepath,
                line=sig.line_start,
                old_signature=sig,
            ))

        # 修改的 API
        for name in sorted(old_names & new_names):
            old_sig = old_sigs[name]
            new_sig = new_sigs[name]

            param_changes = self._compare_parameters(old_sig, new_sig)
            return_change = self._compare_return_type(old_sig, new_sig)

            all_changes = param_changes + ([return_change] if return_change else [])

            if all_changes:
                # 取最严重的级别
                max_level = max(
                    (c.level for c in all_changes),
                    key=lambda l: [ChangeLevel.SAFE, ChangeLevel.WARNING, ChangeLevel.BREAKING].index(l),
                )
                report.changes.append(APIChange(
                    qualified_name=name,
                    change_type="modified",
                    level=max_level,
                    file_path=filepath,
                    line=new_sig.line_start,
                    details=all_changes,
                    old_signature=old_sig,
                    new_signature=new_sig,
                ))

        return report

    def _compare_parameters(
        self, old_sig: APISignature, new_sig: APISignature
    ) -> list[ParameterChange]:
        """逐参数对比两个签名。

        Args:
            old_sig: 旧版本签名。
            new_sig: 新版本签名。

        Returns:
            ParameterChange 列表。
        """
        changes: list[ParameterChange] = []

        old_params = {p.name: p for p in old_sig.parameters if p.name != "self"}
        new_params = {p.name: p for p in new_sig.parameters if p.name != "self"}

        old_names = set(old_params.keys())
        new_names = set(new_params.keys())

        # 新增参数
        for name in new_names - old_names:
            param = new_params[name]
            # 有默认值 = 可选参数 = SAFE；无默认值 = 必需参数 = BREAKING
            if param.default is not None or param.kind in ("VAR_POSITIONAL", "VAR_KEYWORD"):
                level = ChangeLevel.SAFE
            else:
                level = ChangeLevel.BREAKING

            changes.append(ParameterChange(
                param_name=name,
                change_type="added",
                new_value=self._param_repr(param),
                level=level,
            ))

        # 删除参数
        for name in old_names - new_names:
            param = old_params[name]
            changes.append(ParameterChange(
                param_name=name,
                change_type="removed",
                old_value=self._param_repr(param),
                level=ChangeLevel.BREAKING,
            ))

        # 共有参数的变更
        for name in old_names & new_names:
            old_p = old_params[name]
            new_p = new_params[name]

            # 类型注解变更
            if old_p.annotation != new_p.annotation:
                changes.append(ParameterChange(
                    param_name=name,
                    change_type="type_changed",
                    old_value=old_p.annotation or "无注解",
                    new_value=new_p.annotation or "无注解",
                    level=ChangeLevel.WARNING,
                ))

            # 默认值变更
            if old_p.default != new_p.default:
                if old_p.default is not None and new_p.default is None:
                    # 从可选变为必需 → BREAKING
                    level = ChangeLevel.BREAKING
                elif old_p.default is None and new_p.default is not None:
                    # 从必需变为可选 → SAFE
                    level = ChangeLevel.SAFE
                else:
                    # 默认值改变 → WARNING
                    level = ChangeLevel.WARNING

                changes.append(ParameterChange(
                    param_name=name,
                    change_type="default_changed",
                    old_value=old_p.default or "无默认值",
                    new_value=new_p.default or "无默认值",
                    level=level,
                ))

        return changes

    def _compare_return_type(
        self, old_sig: APISignature, new_sig: APISignature
    ) -> ParameterChange | None:
        """对比返回类型注解。

        Args:
            old_sig: 旧版本签名。
            new_sig: 新版本签名。

        Returns:
            如果有变化返回 ParameterChange，否则 None。
        """
        if old_sig.return_annotation != new_sig.return_annotation:
            return ParameterChange(
                param_name="<return>",
                change_type="type_changed",
                old_value=old_sig.return_annotation or "无注解",
                new_value=new_sig.return_annotation or "无注解",
                level=ChangeLevel.BREAKING,
            )
        return None

    def _param_repr(self, param: ParameterInfo) -> str:
        """生成参数的可读表示。

        Args:
            param: 参数信息。

        Returns:
            如 "name: int = 0"
        """
        parts = [param.name]
        if param.annotation:
            parts.append(f": {param.annotation}")
        if param.default:
            parts.append(f" = {param.default}")
        return "".join(parts)
