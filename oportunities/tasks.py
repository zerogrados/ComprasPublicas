from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Oportunidad
from .utilities.update_oportunities import updateOportunity
import logging
import datetime
from oportunities.utilities.insert_oportunities import get_request

logging.basicConfig(filename='../update_oportunities.log', level=logging.ERROR)


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
