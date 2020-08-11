from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Oportunidad
import requests
import json
import logging
import datetime
from oportunities.utilities.insert_oportunities import get_request

logging.basicConfig(filename='../update_oportunities.log',level=logging.ERROR)

def updateOportunity(oportunity):
    """This method update oportunity in database.
    """
    # Check source of oportunity, 1: SECOPI, 2: SECOPII
    if oportunity[1] == 1:
        response = requests.get('https://www.datos.gov.co/resource/c82b-7jfi.json?numero_de_constancia={}'.format(oportunity[0]))
        resp = response.json()[0]
        process = Oportunidad.objects.filter(num_proceso=oportunity[0]).update(estado_proceso=resp['estado_del_proceso'])

@shared_task
def insertOportunitiesToUpdate():
    ''' This method send query to the database to get oportunities ID's for check updates.
    '''
    oportunities = Oportunidad.objects.filter().values_list('num_proceso', 'fuente')
    for oportunity in oportunities:
        try:
            updateOportunity(oportunity)
        except:
            logging.error('Oportunity cannot be update: ' + oportunity[0])
            
@shared_task
def insertOportunities():
    for day in range(3):
        # Check the API for each day since one month ago
        date = (datetime.datetime.today() -
                datetime.timedelta(days=day)).strftime('%m/%d/%Y')
        
        get_request(date)