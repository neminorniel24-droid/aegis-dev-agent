from aegis_agent.inspector import inspect_project
from aegis_agent.planner import create_plan
from aegis_agent.task import DevelopmentTask


def test_create_plan_contains_steps():
    task = DevelopmentTask.create("Add trajectory tracking")
    context = inspect_project()

    plan = create_plan(task, context)

    assert plan.task is task
    assert len(plan.steps) >= 5
    assert "Run the complete pytest suite." in plan.steps


def test_tracking_task_gets_tracking_step():
    task = DevelopmentTask.create("Improve tracking")
    context = inspect_project()

    plan = create_plan(task, context)

    assert any("Track and TrackManager" in step for step in plan.steps)


def test_dashboard_task_gets_dashboard_step():
    task = DevelopmentTask.create("Improve dashboard")
    context = inspect_project()

    plan = create_plan(task, context)

    assert any("dashboard components" in step.lower() for step in plan.steps)
