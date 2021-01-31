from app import app
from celery import Signature


@app.task
def task_a(whatever: str):
    print(whatever)


@app.task
def task_b(whatever: str):
    print(whatever)


def build_chain(arg1, arg2, on_success, on_failure):
    return task_a.si(arg1).on_error(on_failure) | \
        task_b.si(arg2).on_error(on_failure) | \
        on_success


@app.task
def big_task(on_success_name, on_failure_name, *args):
    """This task chains the other two with some orchestration work."""
    on_success = Signature(on_success_name, args=args)
    on_failure = Signature(on_failure_name, args=args)
    chain = build_chain('hello', 'world', on_success, on_failure)
    chain()
