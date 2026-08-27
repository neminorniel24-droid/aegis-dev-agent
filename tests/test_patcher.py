import pytest

from aegis_agent.patcher import FileChange, apply_changes, validate_changes
from aegis_agent.workspace import Workspace


def test_validate_changes_accepts_safe_path():
    changes = [
        FileChange(
            path="tracking/example.py",
            content="print('ok')\n",
        )
    ]

    validate_changes(changes)


def test_validate_changes_rejects_absolute_path():
    with pytest.raises(ValueError, match="Absolute"):
        validate_changes(
            [
                FileChange(
                    path="/tmp/example.py",
                    content="test",
                )
            ]
        )


def test_validate_changes_rejects_parent_path():
    with pytest.raises(ValueError, match="Parent"):
        validate_changes(
            [
                FileChange(
                    path="../example.py",
                    content="test",
                )
            ]
        )


def test_validate_changes_rejects_empty_content():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_changes(
            [
                FileChange(
                    path="example.py",
                    content="",
                )
            ]
        )


def test_apply_changes_uses_workspace(tmp_path):
    workspace_root = tmp_path / "air-aegis"
    workspace_root.mkdir()

    workspace = Workspace(root=workspace_root)

    changes = [
        FileChange(
            path="tracking/example.py",
            content="VALUE = 42\n",
        )
    ]

    apply_changes(workspace, changes)

    assert workspace.read("tracking/example.py") == "VALUE = 42\n"
