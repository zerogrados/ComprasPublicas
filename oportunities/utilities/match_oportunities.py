from oportunities.models import Oportunidad
from accounts.models import Perfil, Usuario


def matchOportunities(perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    # Creates the range bidget filter
    budget_range = [perfil.presupuesto_min, perfil.presupuesto_max]
    # Creates cities list filter
    citites = retrieveProfileCitiesIDs(perfil)    
    oportunities_match = Oportunidad.objects.filter(valor_proceso__range=budget_range,
                                                    municipio_ejecucion__in=citites)
    print(oportunities_match)


def retrieveProfileCitiesIDs(profile):
    cities = []
    for city in profile.ciudad.all():
        cities.append(city.codigo_ciudad)
    return cities
