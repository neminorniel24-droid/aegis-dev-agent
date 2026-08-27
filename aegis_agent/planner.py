"""Development planning for the Aegis Dev Agent."""

from dataclasses import dataclass

from aegis_agent.inspector import ProjectContext
from aegis_agent.task import DevelopmentTask


@dataclass
class TaskPlan:
    """A lightweight execution plan for a development task."""

    task: DevelopmentTask
    steps: list[str]


def create_plan(
    task: DevelopmentTask,
    context: ProjectContext,
) -> TaskPlan:
    """Create a plan using the current Air Aegis project structure."""
    steps = [
        "Inspect the relevant existing implementation.",
        "Identify the smallest appropriate module to change.",
        "Implement the requested capability.",
        "Add or update automated tests.",
        "Run Python syntax validation.",
        "Run the complete pytest suite.",
        "Review the resulting Git diff.",
        "Commit the completed change.",
    ]

    if "dashboard" in task.description.lower():
        steps.insert(
            2,
            "Review the dashboard components before modifying the UI.",
        )

    if "sensor" in task.description.lower():
        steps.insert(
            2,
            "Review the existing sensor and tracking interfaces.",
        )

    if "tracking" in task.description.lower():
        steps.insert(
            2,
            "Review the existing Track and TrackManager interfaces.",
        )

    if not context.files:
        raise ValueError("Air Aegis project contains no files.")

    return TaskPlan(task=task, steps=steps)
