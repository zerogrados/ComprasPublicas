from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from .models import Oportunidad
from .utilities.update_oportunities import updateOportunity
import logging
import datetime
from oportunities.utilities.insert_oportunities import get_request
from accounts.models import Perfil
from oportunities.utilities.match_oportunities import matchOportunities
import redis
import os
import json
from rq import Queue
from datetime import timedelta
import time

logging.basicConfig(filename='../update_oportunities.log', level=logging.ERROR)


@shared_task
def insertOportunitiesToUpdateTask():
    ''' This method send query to the database to get oportunities ID's for check updates.
    '''
    oportunities = Oportunidad.objects.filter().values_list('num_proceso', 'fuente')
    for oportunity in oportunities:
        try:
            updateOportunity(oportunity)
        except:
            logging.error('Oportunity cannot be update: ' + oportunity[0])


@shared_task
def insertOportunitiesTask():
    for day in range(3):
        # Check the API for each day since one month ago
        date = (datetime.datetime.today() -
                datetime.timedelta(days=day)).strftime('%m/%d/%Y')

        get_request(date)

@shared_task
def matchOportunitiesTask():
    perfiles = Perfil.objects.all()
    for perfil in perfiles:
        message = matchOportunities(perfil.id)
        send_message = sendMessageToQueueTask.subtask()
        send_message.delay(message)

@task
def sendMessageToQueueTask(message):
    print(message)
    
    
    
