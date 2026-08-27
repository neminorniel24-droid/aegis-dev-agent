"""Command-line interface for the Aegis Dev Agent."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="aegis-agent",
    help="AI-assisted GitHub development automation tool.",
)
console = Console()


@app.command()
def status() -> None:
    """Show the configured Air Aegis repository."""
    repo = Path.home() / "projects" / "air-aegis"

    if not repo.exists():
        console.print("[red]Air Aegis repository not found.[/red]")
        raise typer.Exit(code=1)

    console.print(
        Panel(
            f"[bold]Air Aegis[/bold]\n{repo}",
            title="Aegis Dev Agent",
        )
    )


@app.command()
def hello() -> None:
    """Verify that the agent is working."""
    console.print(
        "[bold green]Aegis Dev Agent is running.[/bold green]"
    )


def main() -> None:
    """Launch the CLI."""
    app()


if __name__ == "__main__":
    main()


@app.command()
def files() -> None:
    """List files in the Air Aegis repository."""
    from aegis_agent.workspace import Workspace

    workspace = Workspace()

    for file_path in workspace.list_files():
        console.print(file_path)


@app.command()
def read(path: str) -> None:
    """Read a file from the Air Aegis repository."""
    from aegis_agent.workspace import Workspace

    workspace = Workspace()
    console.print(workspace.read(path))


@app.command()
def task(description: str) -> None:
    """Create and display an Air Aegis development task."""
    from aegis_agent.task import DevelopmentTask

    development_task = DevelopmentTask.create(description)

    console.print(
        Panel(
            f"[bold]Task[/bold]\n{development_task.description}\n\n"
            f"[dim]Created: {development_task.created_at}[/dim]",
            title="CommitPilot Task",
        )
    )


@app.command()
def inspect() -> None:
    """Inspect the Air Aegis project."""
    from aegis_agent.inspector import inspect_project

    context = inspect_project()

    console.print(
        Panel(
            f"[bold]Files:[/bold] {len(context.files)}\n\n"
            + "\n".join(context.files[:40])
            + (
                "\n... "
                f"({len(context.files) - 40} more)"
                if len(context.files) > 40
                else ""
            )
            + "\n\n[bold]README:[/bold]\n"
            + context.readme[:1500],
            title="CommitPilot Inspection",
        )
    )


@app.command()
def plan(description: str) -> None:
    """Create an execution plan for an Air Aegis task."""
    from aegis_agent.inspector import inspect_project
    from aegis_agent.planner import create_plan
    from aegis_agent.task import DevelopmentTask

    task_obj = DevelopmentTask.create(description)
    context = inspect_project()
    task_plan = create_plan(task_obj, context)

    console.print(
        Panel(
            "\n".join(
                f"[bold]{index}.[/bold] {step}"
                for index, step in enumerate(task_plan.steps, 1)
            ),
            title=f"Plan: {task_obj.description}",
        )
    )


@app.command()
def run(
    description: str,
    apply: bool = typer.Option(
        False,
        "--apply",
        help="Apply the AI-generated patch.",
    ),
) -> None:
    """Generate and optionally apply an Air Aegis implementation."""
    from aegis_agent.inspector import inspect_project
    from aegis_agent.planner import create_plan
    from aegis_agent.task import DevelopmentTask

    task_obj = DevelopmentTask.create(description)
    context = inspect_project()
    task_plan = create_plan(task_obj, context)

    console.print(
        Panel(
            "\n".join(
                f"[bold]{index}.[/bold] {step}"
                for index, step in enumerate(task_plan.steps, 1)
            ),
            title="Execution Plan",
        )
    )

    if not apply:
        console.print(
            "\n[yellow]Dry run only.[/yellow] "
            "Use --apply to generate and apply the implementation."
        )
        return

    console.print("\n[bold]Generating implementation...[/bold]")

    from aegis_agent.runner import execute_task

    changes = execute_task(description)

    console.print(
        f"[green]Generated {len(changes)} file change(s).[/green]"
    )

    for change in changes:
        console.print(f"  • {change.path}")

    console.print("\n[bold]Running Air Aegis tests...[/bold]")

    from aegis_agent.executor import Executor

    result = Executor().run(["pytest", "-q"])

    if result.stdout:
        console.print(result.stdout)

    if result.returncode != 0:
        console.print(
            "[red]Tests failed. Changes were applied but NOT committed.[/red]"
        )
        raise typer.Exit(code=1)

    console.print(
        "[bold green]Implementation applied and tests passed.[/bold green]"
    )


@app.command("git-status")
def git_status() -> None:
    """Show Git status for the configured target repository."""
    from commitpilot_git import GitManager

    from pathlib import Path

    repo = Path.home() / "projects" / "air-aegis"
    manager = GitManager(repo)
    status = manager.status()

    console.print(
        Panel(
            f"[bold]Branch:[/bold] {status.branch}\n"
            f"[bold]Clean:[/bold] {status.clean}\n"
            + (
                "\n[bold]Changes:[/bold]\n"
                + "\n".join(status.changes)
                if status.changes
                else "\n[bold]Changes:[/bold] none"
            ),
            title="CommitPilot Git Status",
        )
    )
