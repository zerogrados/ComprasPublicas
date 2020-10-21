# Celery
from __future__ import absolute_import, unicode_literals
from celery import shared_task

# Models
from .models import Subscription

# Utils
import datetime

@shared_task
def updateSubscriptionsTask():
    """
    This method update Subscription status to false when finalize to subscription time.
    """
    date = datetime.datetime.today() - datetime.timedelta(days=1)
    Subscription.objects.filter(end_date__lte=date, active=True).update(active=False)