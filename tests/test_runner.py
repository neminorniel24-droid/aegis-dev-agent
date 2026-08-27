def test_build_context_contains_air_aegis_files():
    from aegis_agent.runner import build_context

    context = build_context()

    assert "README.md" in context
    assert "tracking" in context


def test_execute_task_is_importable():
    from aegis_agent.runner import execute_task

    assert callable(execute_task)
