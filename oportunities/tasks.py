from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from .models import Oportunidad
from .utilities.update_oportunities import updateOportunity
import logging
import datetime
from oportunities.utilities.insert_oportunities import get_request
from accounts.models import Perfil
from oportunities.utilities.match_oportunities import matchOportunities, NewOportunitiesInfo
from accounts.models import Usuario
import redis
import os
import json
from datetime import timedelta
from django.template import loader


logging.basicConfig(filename='../update_oportunities.log', level=logging.ERROR)


@shared_task
def insertOportunitiesToUpdateTask():
    ''' This method send query to the database to get oportunities ID's for check updates.
    '''
    oportunities = Oportunidad.objects.filter().values_list('num_proceso', 'fuente')
    for oportunity in oportunities:
        try:
            updateOportunity(oportunity)
        except Exception as e:
            logging.error('Oportunity cannot be update: ' + oportunity[0] + ': ' +  e)


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
        send_message = sendMatchEmailTask.subtask()
        send_message.delay(message)


@task
def sendMatchEmailTask(message):
    mail_data = NewOportunitiesInfo(message)
    name, email = mail_data.getUserData()
    oportunities = mail_data.getOportunities()
    
    from django.core.mail import send_mail
    from django.conf import settings
    from django.contrib.sites.models import Site
    
    if len(oportunities) > 0:
        domain = Site.objects.get_current().domain
        n_oportunities = str(len(oportunities))
        if len(oportunities) > 3:
            oportunities = oportunities[:3]
        html_message = loader.render_to_string('oportunities/new_oportunities.html',
                                                {
                                                    'user_name': name,
                                                    'oportunities': oportunities,
                                                    'n_oportunities': n_oportunities,
                                                    'domain': domain
                                                }
                                              )
        send_mail(
            'Nuevas oportunidades',
            '',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
    else:
        send_mail(
            'Nuevas oportunidades',
            'No tienes nuevas oportunidades. Aprende a configurar aquí',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )