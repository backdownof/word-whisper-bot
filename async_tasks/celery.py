import os
import celery
from celery import Celery

from db import models

from dotenv import load_dotenv

load_dotenv()

CELERY_HOST = os.getenv('CELERY_HOST')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASS = os.getenv('REDIS_PASS')
REDIS_EXPOSED_PORT = os.getenv('REDIS_EXPOSED_PORT')

app = Celery(
    'async_tasks',
    broker=f'redis://default:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/1',
    include=['async_tasks.periodic.tasks'],
)

app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

app.conf.beat_schedule = {
    'daily_word_task': {
        'task': 'async_tasks.periodic.tasks.send_daily_word',
        'schedule': 15,
    },
}


class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        models.DBSession.remove()
