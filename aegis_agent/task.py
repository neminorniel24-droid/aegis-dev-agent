"""Task handling for the Aegis Dev Agent."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class DevelopmentTask:
    """A development task for Air Aegis."""

    description: str
    created_at: str

    @classmethod
    def create(cls, description: str) -> "DevelopmentTask":
        """Create a validated development task."""
        description = description.strip()

        if not description:
            raise ValueError("Task description must not be empty.")

        return cls(
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
