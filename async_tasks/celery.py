import datetime

from async_tasks.constants import DailyWordTask
from config import App
from db import models

import celery
from celery import Celery
from celery.schedules import crontab


app = Celery(
    "async_tasks",
    broker=f"{App.config('REDIS_URI')}/1",
    include=["async_tasks.periodic.tasks"],
)

app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=3600,
    enable_utc=True,
    timezone=datetime.timezone.utc,
)

app.conf.beat_schedule = {
    'daily_word_task': {
        'task': 'async_tasks.periodic.tasks.send_daily_word',
        'schedule': crontab(hour=str(DailyWordTask.UTC_HOUR), minute='0')
        # 'schedule': 15,
    },
}


class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        models.DBSession.remove()
