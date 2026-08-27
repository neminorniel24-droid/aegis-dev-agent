"""Safe workspace operations for the Aegis Dev Agent."""

from pathlib import Path


class Workspace:
    """Provide controlled access to the Air Aegis repository."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or (Path.home() / "projects" / "air-aegis")

        if not self.root.exists():
            raise FileNotFoundError(
                f"Air Aegis repository not found: {self.root}"
            )

    def resolve(self, relative_path: str) -> Path:
        """Resolve a path while preventing access outside the repository."""
        path = (self.root / relative_path).resolve()

        try:
            path.relative_to(self.root.resolve())
        except ValueError as exc:
            raise ValueError(
                "Path must remain inside the Air Aegis repository."
            ) from exc

        return path

    def read(self, relative_path: str) -> str:
        """Read a text file from Air Aegis."""
        path = self.resolve(relative_path)

        if not path.is_file():
            raise FileNotFoundError(relative_path)

        return path.read_text()

    def write(self, relative_path: str, content: str) -> None:
        """Write a text file inside Air Aegis."""
        path = self.resolve(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def exists(self, relative_path: str) -> bool:
        """Check whether a path exists."""
        return self.resolve(relative_path).exists()

    def list_files(self) -> list[str]:
        """Return repository files excluding Git and virtual environments."""
        files = []

        for path in self.root.rglob("*"):
            if not path.is_file():
                continue

            relative = path.relative_to(self.root)

            if any(part in {".git", ".venv", "__pycache__"} for part in relative.parts):
                continue

            files.append(str(relative))

        return sorted(files)
