from celery import task
from app import app


def app_context_task(run_func):
    @task
    def task_wrapper(*args, **kwargs):
        with app.app_context():
            return run_func(*args, **kwargs)

    return task_wrapper
