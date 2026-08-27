from typer.testing import CliRunner

from aegis_agent.cli import app


runner = CliRunner()


def test_hello_command():
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "Aegis Dev Agent is running." in result.stdout


def test_status_command():
    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0


def test_git_status_command():
    result = runner.invoke(app, ["git-status"])

    assert result.exit_code == 0
    assert "CommitPilot Git Status" in result.stdout
