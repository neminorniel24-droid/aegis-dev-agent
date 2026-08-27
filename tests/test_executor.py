from aegis_agent.executor import Executor


def test_executor_runs_in_air_aegis():
    executor = Executor()

    result = executor.run(
        ["python", "-c", "print('air-aegis-ok')"]
    )

    assert result.returncode == 0
    assert "air-aegis-ok" in result.stdout


def test_executor_runs_pytest():
    executor = Executor()

    result = executor.run(["pytest", "-q"])

    assert result.returncode == 0
