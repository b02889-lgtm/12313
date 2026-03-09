"""
API Diff 报告输出模块

使用 rich 库在终端输出彩色的 API 变更报告。
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from guardian.modules.api_diff import APIChange, ChangeLevel, DiffReport


# 级别对应的颜色和图标
LEVEL_STYLES = {
    ChangeLevel.SAFE: ("green", "✅"),
    ChangeLevel.WARNING: ("yellow", "⚠️"),
    ChangeLevel.BREAKING: ("red bold", "❌"),
}


class APIDiffReporter:
    """API Diff 彩色报告输出器"""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_report(self, report: DiffReport) -> None:
        """打印完整的 API Diff 报告。

        Args:
            report: DiffReport 实例。
        """
        if not report.changes:
            self.console.print(
                Panel(
                    f"[green]✅ {report.file_path}: 无公开 API 变更[/green]",
                    border_style="green",
                )
            )
            return

        # 标题面板
        stats = report.stats
        level_style, level_icon = LEVEL_STYLES[report.max_level]
        title = Text(f"{level_icon} API Diff: {report.file_path}", style=level_style)

        self.console.print()
        self.console.print(Panel(title, border_style=level_style.split()[0]))

        # 统计摘要
        summary_parts = []
        if stats["added"]:
            summary_parts.append(f"[green]+{stats['added']} 新增[/green]")
        if stats["removed"]:
            summary_parts.append(f"[red]-{stats['removed']} 删除[/red]")
        if stats["modified"]:
            summary_parts.append(f"[yellow]~{stats['modified']} 修改[/yellow]")

        self.console.print("  " + "  ".join(summary_parts))
        self.console.print()

        # 详细变更表格
        table = Table(show_header=True, header_style="bold", expand=True)
        table.add_column("级别", width=8, justify="center")
        table.add_column("类型", width=6, justify="center")
        table.add_column("API 名称", min_width=20)
        table.add_column("详情", min_width=30)

        for change in report.changes:
            style, icon = LEVEL_STYLES[change.level]
            level_text = Text(f"{icon} {change.level.value}", style=style)

            type_map = {"added": "[green]新增[/green]", "removed": "[red]删除[/red]", "modified": "[yellow]修改[/yellow]"}
            type_text = type_map.get(change.change_type, change.change_type)

            detail_text = self._format_change_details(change)

            table.add_row(level_text, type_text, change.qualified_name, detail_text)

        self.console.print(table)
        self.console.print()

    def print_multi_file_report(self, reports: list[DiffReport]) -> None:
        """打印多文件汇总报告。

        Args:
            reports: DiffReport 列表。
        """
        non_empty = [r for r in reports if r.changes]

        if not non_empty:
            self.console.print(
                Panel("[green]✅ 暂存区中无公开 API 变更[/green]", border_style="green")
            )
            return

        # 汇总统计
        total_breaking = sum(r.stats["breaking"] for r in non_empty)
        total_warning = sum(r.stats["warning"] for r in non_empty)
        total_safe = sum(r.stats["safe"] for r in non_empty)

        self.console.print()
        self.console.rule("[bold]Guardian APIDiff 报告[/bold]")
        self.console.print(
            f"  检测到 [bold]{len(non_empty)}[/bold] 个文件有 API 变更  "
            f"[red]{total_breaking} BREAKING[/red]  "
            f"[yellow]{total_warning} WARNING[/yellow]  "
            f"[green]{total_safe} SAFE[/green]"
        )
        self.console.print()

        for report in non_empty:
            self.print_report(report)

        # 最终结论
        if total_breaking > 0:
            self.console.print(
                Panel(
                    f"[red bold]❌ 发现 {total_breaking} 个破坏性 API 变更！请仔细检查。[/red bold]",
                    border_style="red",
                )
            )
        elif total_warning > 0:
            self.console.print(
                Panel(
                    f"[yellow]⚠️ 发现 {total_warning} 个警告级别的 API 变更。[/yellow]",
                    border_style="yellow",
                )
            )
        else:
            self.console.print(
                Panel("[green]✅ 所有 API 变更均为安全级别。[/green]", border_style="green")
            )

    def _format_change_details(self, change: APIChange) -> str:
        """格式化变更详情。

        Args:
            change: APIChange 实例。

        Returns:
            格式化的详情字符串。
        """
        if change.change_type == "added":
            if change.new_signature:
                params = ", ".join(
                    p.name for p in change.new_signature.parameters if p.name != "self"
                )
                ret = f" -> {change.new_signature.return_annotation}" if change.new_signature.return_annotation else ""
                return f"({params}){ret}"
            return "新增 API"

        if change.change_type == "removed":
            return "API 已删除"

        # modified
        parts = []
        for detail in change.details:
            style, _ = LEVEL_STYLES[detail.level]
            if detail.change_type == "added":
                parts.append(f"[{style}]+参数 {detail.param_name}: {detail.new_value}[/{style}]")
            elif detail.change_type == "removed":
                parts.append(f"[{style}]-参数 {detail.param_name}[/{style}]")
            elif detail.change_type == "type_changed":
                parts.append(f"[{style}]{detail.param_name}: {detail.old_value} → {detail.new_value}[/{style}]")
            elif detail.change_type == "default_changed":
                parts.append(f"[{style}]{detail.param_name} 默认值: {detail.old_value} → {detail.new_value}[/{style}]")
        return "\n".join(parts) if parts else "有变更"
