"""High-level task execution for Air Aegis."""

from aegis_agent.ai import AIClient
from aegis_agent.inspector import inspect_project
from aegis_agent.patcher import FileChange, apply_changes
from aegis_agent.task import DevelopmentTask
from aegis_agent.workspace import Workspace


def build_context() -> str:
    """Build bounded repository context for the coding model."""
    workspace = Workspace()
    files = workspace.list_files()

    relevant = []

    for path in files:
        if path.startswith("tests/") or path.endswith(".py"):
            try:
                content = workspace.read(path)
            except Exception:
                continue

            if len(content) > 12000:
                content = content[:12000] + "\n# [truncated]"

            relevant.append(
                f"\n===== {path} =====\n{content}"
            )

    context = "\n".join(relevant)

    return context[:60000]


def execute_task(description: str) -> list[FileChange]:
    """Generate and apply a validated implementation patch."""
    task = DevelopmentTask.create(description)
    context = build_context()

    client = AIClient()
    changes = client.generate_patch(
        task=task.description,
        context=context,
    )

    file_changes = [
        FileChange(
            path=item["path"],
            content=item["content"],
        )
        for item in changes
    ]

    workspace = Workspace()
    apply_changes(workspace, file_changes)

    return file_changes
