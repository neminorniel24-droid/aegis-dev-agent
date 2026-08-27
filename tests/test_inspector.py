from aegis_agent.inspector import inspect_project


def test_inspect_project_finds_files():
    context = inspect_project()

    assert context.files
    assert "README.md" in context.files


def test_inspect_project_reads_readme():
    context = inspect_project()

    assert isinstance(context.readme, str)
    assert context.readme
