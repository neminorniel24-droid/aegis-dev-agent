from pathlib import Path

import pytest

from aegis_agent.workspace import Workspace


def test_workspace_points_to_air_aegis():
    workspace = Workspace()

    assert workspace.root.exists()
    assert workspace.root.name == "air-aegis"


def test_workspace_lists_project_files():
    workspace = Workspace()

    files = workspace.list_files()

    assert isinstance(files, list)
    assert "README.md" in files


def test_workspace_rejects_paths_outside_repo():
    workspace = Workspace()

    with pytest.raises(ValueError):
        workspace.resolve("../outside.txt")


def test_workspace_can_read_readme():
    workspace = Workspace()

    content = workspace.read("README.md")

    assert isinstance(content, str)
    assert len(content) > 0


def test_workspace_write_and_read(tmp_path):
    workspace_root = tmp_path / "air-aegis"
    workspace_root.mkdir()

    workspace = Workspace(root=workspace_root)
    workspace.write("test.txt", "hello")

    assert workspace.read("test.txt") == "hello"
