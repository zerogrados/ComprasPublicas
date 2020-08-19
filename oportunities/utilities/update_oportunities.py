import json
import requests

# Modelo
from oportunities.models import Oportunidad

def updateOportunity(oportunity):
    """This method update oportunity in database.
    """
    # Check source of oportunity, 1: SECOPI, 2: SECOPII
    if oportunity[1] == 1:
        response = requests.get(
            'https://www.datos.gov.co/resource/c82b-7jfi.json?numero_de_constancia={}'.format(oportunity[0]))
        resp = response.json()[0]
        process = Oportunidad.objects.filter(num_proceso=oportunity[0]).update(
            estado_proceso=resp['estado_del_proceso'])