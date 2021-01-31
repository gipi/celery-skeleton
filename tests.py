"""
Test the tasks
"""
from foo.tasks import task_a, big_task


def test_task_a(mocker):
    """Some operations"""
    task_a.apply()

    assert True


# here an example on using mocker fixture instead of mock.patch
# that doesn't seem to work with the tasks, probably cause of
# some aspects of the importing mechanism inside celery
def test_big_task_create_chain(celery_app, mocker):
    """Check big_task create the correct signatures."""
    mocked_task_a = mocker.patch('foo.tasks.task_a')
    mocked_task_b = mocker.patch('foo.tasks.task_b')

    @celery_app.task
    def on_success(*args):
        print("OK")

    @celery_app.task
    def on_failure(*args):
        print("FAILURE")

    big_task.apply((on_success, on_failure))

    assert mocked_task_a.si.called
    assert mocked_task_b.si.called
