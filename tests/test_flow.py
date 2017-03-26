import pytest
import prefect.exceptions
import prefect
from prefect.flow import Flow



def test_create_flow():

    # name is required
    with pytest.raises(TypeError) as e:
        Flow()
    err = "__init__() missing 1 required positional argument: 'name'"
    assert err in str(e)

    # name must be a string
    with pytest.raises(TypeError) as e:
        f = Flow(name=1)
    assert 'Name must be a string' in str(e)

    f = Flow('test')


def test_cycle_detection():
    """
    Test that cycles are detected
    """
    f = Flow('test')
    # use integers as dummy tasks
    f.graph[1] = set()
    f.graph[2] = set([1])
    f.graph[3] = set([2, 1])
    tasks = f.sorted_tasks()

    # introduce a cycle
    f.graph[2].add(3)
    with pytest.raises(prefect.exceptions.PrefectError) as e:
        tasks = f.sorted_tasks()
    assert 'Cycle detected' in str(e)


def test_get_task_by_name():
    with Flow('test') as f:
        t1 = prefect.task.Task(fn=lambda: 1, name='t1')
        t2 = prefect.task.Task(fn=lambda: 1, name='t2')
        t1.run_before(t2)

    assert f.get_task('t1') is t1
    with pytest.raises(PrefectError):
        f.get_task('some task')
