"""Command-line interface for the Aegis Dev Agent."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="aegis-agent",
    help="Local development assistant for Air Aegis.",
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
