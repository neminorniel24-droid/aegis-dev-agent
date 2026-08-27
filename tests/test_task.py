import pytest

from aegis_agent.task import DevelopmentTask


def test_task_creation():
    task = DevelopmentTask.create("Add trajectory tracking")

    assert task.description == "Add trajectory tracking"
    assert task.created_at


def test_task_strips_whitespace():
    task = DevelopmentTask.create("  Improve sensors  ")

    assert task.description == "Improve sensors"


def test_task_rejects_empty_description():
    with pytest.raises(ValueError, match="must not be empty"):
        DevelopmentTask.create("   ")
