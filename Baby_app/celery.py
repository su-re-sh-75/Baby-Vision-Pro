from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baby.settings')

app = Celery('Baby_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-sensor-stats-data-every-2-seconds': {
        'task': 'Baby_app.tasks.send_sensor_data_stats',
        'schedule': 2.0,
    },
    'send-sensor-data-every-2-seconds':{
        'task': 'Baby_app.tasks.send_sensor_data',
        'schedule': 2.0,
    }
}
