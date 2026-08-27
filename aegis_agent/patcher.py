"""Safe patch generation and application for Air Aegis."""

from dataclasses import dataclass


@dataclass
class FileChange:
    """A single file replacement inside Air Aegis."""

    path: str
    content: str


def validate_changes(changes: list[FileChange]) -> None:
    """Validate that generated changes use safe repository paths."""
    if not changes:
        raise ValueError("At least one file change is required.")

    for change in changes:
        path = change.path.strip()

        if not path:
            raise ValueError("Change path must not be empty.")

        if path.startswith("/"):
            raise ValueError("Absolute paths are not allowed.")

        parts = path.replace("\\", "/").split("/")

        if ".." in parts:
            raise ValueError("Parent-directory paths are not allowed.")

        if not change.content:
            raise ValueError(
                f"File content must not be empty: {change.path}"
            )


def apply_changes(workspace, changes: list[FileChange]) -> None:
    """Apply validated file changes to the Air Aegis workspace."""
    validate_changes(changes)

    for change in changes:
        workspace.write(change.path, change.content)
