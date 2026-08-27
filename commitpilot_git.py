"""Git operations for CommitPilot."""

from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class GitStatus:
    """Current Git repository state."""

    branch: str
    clean: bool
    changes: list[str]


class GitManager:
    """Safely inspect Git state for a target repository."""

    def __init__(self, repo: Path) -> None:
        self.repo = repo.resolve()

        if not self.repo.exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repo}"
            )

        if not (self.repo / ".git").exists():
            raise ValueError(
                f"Not a Git repository: {self.repo}"
            )

    def _run(self, args: list[str]) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or "Git command failed."
            )

        return result.stdout.strip()

    def branch(self) -> str:
        """Return the current branch name."""
        return self._run(
            ["branch", "--show-current"]
        )

    def status(self) -> GitStatus:
        """Return the current repository status."""
        raw = self._run(
            ["status", "--short"]
        )

        changes = [
            line for line in raw.splitlines()
            if line.strip()
        ]

        return GitStatus(
            branch=self.branch(),
            clean=not changes,
            changes=changes,
        )

    def log(self, count: int = 5) -> list[str]:
        """Return recent commit summaries."""
        if count < 1:
            raise ValueError("count must be positive.")

        raw = self._run(
            ["log", f"-{count}", "--oneline"]
        )

        return raw.splitlines()
