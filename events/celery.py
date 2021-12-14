from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')
app = Celery('events')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.CELERYBEAT_SCHEDULE = {
    'disable_expired_planpurchase': {
        'task': 'applications.payment.tasks.disable_expired_purchase',
        # 'schedule': crontab(minute=0, hour=[0, 6, 12, 18]), # runs at 12am, 6am , 12pm and 6pm every day
        'schedule': crontab(minute="*/1"),
        'kwargs': {'limit_per_run': 10 }
    },
}