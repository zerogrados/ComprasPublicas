from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compras_publicas.settings')

app = Celery('compras_publicas')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Shceduled tasks
app.conf.beat_schedule = {
    'demo-15s': {
        'task': 'oportunities.tasks.async_test',
        'schedule': 15,
        'args': (9, 1)
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))