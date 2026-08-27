"""Task execution support for the Aegis Dev Agent."""

from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class CommandResult:
    """Result from a local development command."""

    command: str
    returncode: int
    stdout: str
    stderr: str


class Executor:
    """Run controlled development commands in Air Aegis."""

    def __init__(self, repo: Path | None = None) -> None:
        self.repo = repo or (
            Path.home() / "projects" / "air-aegis"
        )

        if not self.repo.exists():
            raise FileNotFoundError(
                f"Air Aegis repository not found: {self.repo}"
            )

    def run(self, command: list[str]) -> CommandResult:
        """Run a command inside the Air Aegis repository."""
        executable = self.repo / ".venv" / "bin"

        if command and command[0] in {"python", "pytest"}:
            program = executable / command[0]
            if program.exists():
                command = [str(program), *command[1:]]

        result = subprocess.run(
            command,
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )

        return CommandResult(
            command=" ".join(command),
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
