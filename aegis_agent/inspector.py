"""Repository inspection for the Aegis Dev Agent."""

from dataclasses import dataclass

from aegis_agent.workspace import Workspace


@dataclass
class ProjectContext:
    """Relevant context collected from Air Aegis."""

    files: list[str]
    readme: str


def inspect_project() -> ProjectContext:
    """Collect a lightweight project overview."""
    workspace = Workspace()

    files = workspace.list_files()

    readme = ""
    if workspace.exists("README.md"):
        readme = workspace.read("README.md")

    return ProjectContext(
        files=files,
        readme=readme,
    )
