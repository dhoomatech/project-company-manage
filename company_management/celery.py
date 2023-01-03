from __future__ import absolute_import

import os

from celery import Celery,shared_task
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')

from django.conf import settings  # noqa
from celery.schedules import crontab

app = Celery('company_management')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.result_expires = 1800
app.conf.celery_task_result_expires  = 1800

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
app.conf.beat_schedule = {
    # 'task-one': {
    #     'task': 'afl_commerce.afl_subscriptions.tasks.subscription_job',
    #     'schedule': crontab(minute="*/2"),
    # },  
}