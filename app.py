from celery import Celery

app = Celery('tasks', broker='redis://localhost')

app.conf.imports = (
    'foo.tasks',
)
