from pathlib import Path

import pytest

from commitpilot_git import GitManager


ROOT = Path.home() / "projects" / "air-aegis"


def test_git_manager_reads_branch():
    manager = GitManager(ROOT)

    branch = manager.branch()

    assert branch


def test_git_manager_reads_status():
    manager = GitManager(ROOT)

    status = manager.status()

    assert status.branch
    assert isinstance(status.clean, bool)
    assert isinstance(status.changes, list)


def test_git_manager_reads_log():
    manager = GitManager(ROOT)

    commits = manager.log(3)

    assert commits
    assert len(commits) <= 3


def test_git_manager_rejects_non_git_directory(tmp_path):
    with pytest.raises(ValueError, match="Not a Git repository"):
        GitManager(tmp_path)
