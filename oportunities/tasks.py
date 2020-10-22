# Celery
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task

# Django
from django.db.models import Q
from django.template import loader

# Models
from accounts.models import Usuario, Perfil
from .models import Oportunidad, Favorito

# Utils
import datetime
import logging
import datetime

# Local utils
from oportunities.utilities.insert_oportunities import get_request
from oportunities.utilities.match_oportunities import (
    matchOportunities,
    NewOportunitiesInfo,
)
from .utilities.update_oportunities import updateOportunity

logging.basicConfig(filename="../update_oportunities.log", level=logging.ERROR)


@shared_task
def updateOportunitiesTask():
    """This method send query to the database to get oportunities ID's for check updates."""
    
    oportunities = Oportunidad.objects.filter().values("num_proceso", "fuente")
    for oportunity in oportunities:
        try:
            updateOportunity(oportunity)
        except Exception as e:
            logging.error(
                "Oportunity cannot be update: "
                + oportunity["num_proceso"]
                + ": "
                + str(e)
            )


@shared_task
def insertOportunitiesTask():
    for day in range(3):
        # Check the API for each day since one month ago
        date = datetime.datetime.today() - datetime.timedelta(days=day)

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

    domain = Site.objects.get_current().domain

    if len(oportunities) > 0:
        n_oportunities = str(len(oportunities))
        if len(oportunities) > 3:
            oportunities = oportunities[:3]
        html_message = loader.render_to_string(
            "oportunities/new_oportunities_email.html",
            {
                "user_name": name,
                "oportunities": oportunities,
                "n_oportunities": n_oportunities,
                "domain": domain,
            },
        )
        send_mail(
            "Nuevas oportunidades",
            "",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
    else:
        html_message = loader.render_to_string(
            "oportunities/new_oportunities_email_empty.html",
            {"user_name": name, "domain": domain},
        )
        send_mail(
            "Nuevas oportunidades",
            "",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=html_message,
        )


@task
def addRemoveFavsTask(userId, processId, state):
    # State 0: Remove fav
    # State 1: Add fav
    if state:
        newFav = Favorito(
            usuario=Usuario.objects.get(pk=userId),
            oportunidad=Oportunidad.objects.get(num_proceso=processId),
        )
        try:
            newFav.save()
        except Exception as e:
            logging.warning(
                "Oportunity {} cannot be saved in favs: {}".format(processId, e)
            )
    else:
        try:
            oportunityId = Oportunidad.objects.get(num_proceso=processId).id
            Favorito.objects.get(usuario=userId, oportunidad=oportunityId).delete()
        except Exception as e:
            logging.warning(
                "Cannot delete {} oportunity from favs: {}".format(processId, e)
            )


@shared_task
def deleteOportunitiesTask():
    """
    This method send query to the database to get oportunities ID's for delete in state 'Adjudicado' or 'Celebrado'
    whit a 'fecha_publicacion' date smaller than 31 days ago and that has not been selected as a favorite.
    """
    
    date = datetime.datetime.today() - datetime.timedelta(days=31)
    oportunities_fav = Favorito.objects.all().values_list("oportunidad_id", flat=True)
    Oportunidad.objects.filter(
        (Q(estado_proceso="Adjudicado") | Q(estado_proceso="Celebrado"))
        & ~Q(id__in=oportunities_fav),
        fecha_publicacion__lte=date,
    ).delete()