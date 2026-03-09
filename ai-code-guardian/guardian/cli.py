"""
Guardian CLI 入口模块

提供命令行交互接口，注册所有子命令。
使用 Click 框架构建。
"""

import click
from rich.console import Console

from guardian import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="guardian")
@click.option("--config", "-c", default=None, help="配置文件路径（默认为 .guardian.yaml）")
@click.pass_context
def main(ctx: click.Context, config: str | None) -> None:
    """🛡️ AI Code Guardian - AI 驱动的代码健康守护者

    智能预提交检查工具，在开发阶段自动检测代码质量问题。
    """
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


@main.command()
@click.pass_context
def check(ctx: click.Context) -> None:
    """对暂存区 (staged) 文件执行全量检查

    依次运行所有启用的模块：测试生成、API 对比、性能检测、国际化审查。
    """
    console.print("[bold green]🛡️ AI Code Guardian - 全量检查[/bold green]")
    console.print("─" * 50)

    # TODO: T6.1 统一编排 - 调用所有模块
    console.print("[yellow]⚠️ 全量检查功能将在后续阶段实现[/yellow]")


@main.command(name="test-gen")
@click.option("--file", "-f", default=None, help="指定要生成测试的文件路径")
@click.pass_context
def test_gen(ctx: click.Context, file: str | None) -> None:
    """AI 驱动的测试生成

    分析 staged 文件中新增或修改的函数，自动生成 pytest 单元测试。
    """
    console.print("[bold blue]🧪 AI 测试生成器[/bold blue]")
    console.print("─" * 50)

    # TODO: T4 阶段实现
    console.print("[yellow]⚠️ 测试生成功能将在阶段 4 实现[/yellow]")


@main.command(name="api-diff")
@click.option("--strict/--no-strict", default=None, help="严格模式：破坏性变更时阻断提交")
@click.pass_context
def api_diff(ctx: click.Context, strict: bool | None) -> None:
    """API 破坏性变更检测

    对比 HEAD 和 staged 版本的公开 API 签名，识别破坏性变更。
    """
    console.print("[bold red]🔌 API 破坏性变更检测器[/bold red]")
    console.print("─" * 50)

    # TODO: T2 阶段实现
    console.print("[yellow]⚠️ API 对比功能将在阶段 2 实现[/yellow]")


@main.command()
@click.option("--threshold", "-t", default=None, type=float, help="性能退化阈值（如 0.30 表示 30%）")
@click.pass_context
def perf(ctx: click.Context, threshold: float | None) -> None:
    """性能退化检测

    对比代码修改前后的执行性能，检测可能的退化。
    """
    console.print("[bold magenta]⚡ 性能退化守卫[/bold magenta]")
    console.print("─" * 50)

    # TODO: T5 阶段实现
    console.print("[yellow]⚠️ 性能检测功能将在阶段 5 实现[/yellow]")


@main.command()
@click.option("--auto-replace/--no-auto-replace", default=False, help="自动替换硬编码字符串")
@click.pass_context
def i18n(ctx: click.Context, auto_replace: bool) -> None:
    """国际化硬编码审查

    检测代码中的硬编码中文字符串，提供翻译和替换建议。
    """
    console.print("[bold cyan]🌐 国际化硬编码守卫[/bold cyan]")
    console.print("─" * 50)

    # TODO: T3 阶段实现
    console.print("[yellow]⚠️ 国际化审查功能将在阶段 3 实现[/yellow]")


@main.command(name="install-hook")
@click.pass_context
def install_hook(ctx: click.Context) -> None:
    """安装 Git pre-commit hook

    在当前 Git 仓库中安装 pre-commit 钩子，使 guardian check 在每次提交前自动运行。
    """
    console.print("[bold yellow]📎 Pre-commit Hook 安装器[/bold yellow]")
    console.print("─" * 50)

    # TODO: T6.3 实现
    console.print("[yellow]⚠️ Hook 安装功能将在阶段 6 实现[/yellow]")


if __name__ == "__main__":
    main()
