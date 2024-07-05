from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baby.settings')

app = Celery('Baby_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-notification-data-every-2-seconds': {
        'task': 'Baby_app.tasks.send_notification_data',
        'schedule': 2.0,
    },
}
