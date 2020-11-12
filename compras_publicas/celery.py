from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

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
    'update_subscriptions': {
        'task': 'subscriptions.tasks.updateSubscriptionsTask',
        'schedule': crontab(minute=00, hour=1),
    },    
    'delete_oportunities': {
        'task': 'oportunities.tasks.deleteOportunitiesTask',
        'schedule': crontab(minute=30, hour=1),
    },
    'update_oportunities': {
        'task': 'oportunities.tasks.updateOportunitiesTask',
        'schedule': crontab(minute=00, hour=2),
    },    
    'insert_oportunities': {
        'task': 'oportunities.tasks.insertOportunitiesTask',
        'schedule': crontab(minute=30, hour=2),
    },
    'match_oportunities': {
        'task': 'oportunities.tasks.matchOportunitiesTask',
        'schedule': crontab(minute=00, hour=7),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
