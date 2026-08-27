def test_build_context_contains_tracking_files():
    from aegis_agent.runner import build_context

    context = build_context()

    assert "tracking/track.py" in context
    assert "tracking/manager.py" in context


def test_execute_task_is_importable():
    from aegis_agent.runner import execute_task

    assert callable(execute_task)
