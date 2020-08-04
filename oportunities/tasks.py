from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Oportunidad
import redis

import os
import datetime
import json


def setQueueMsg(oportunities):
    '''This method stablish connection to the queue and set messages
    '''
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_db = os.environ.get('REDIS_DB')
    redis_connection = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    for oportunity in oportunities:
        msg = {'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'num_proceso': oportunity[0],
               'fuente': str(oportunity[1])
               }
        redis_connection.set('oportunity-{}'.format(oportunity[0]), json.dumps(msg))


@shared_task
def insertOportunitiesToUpdate():
    ''' This method send query to the database to get oportunities ID's for check updates.
    The IDs get sended to redis queue.
    '''
    oportunities = Oportunidad.objects.filter().values_list('num_proceso', 'fuente')
    setQueueMsg(oportunities)
