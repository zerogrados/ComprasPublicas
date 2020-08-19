from oportunities.models import Oportunidad
from accounts.models import Perfil, Usuario
from django.db.models import Q


def matchOportunities(perfil_id, user_request=None):
    perfil = Perfil.objects.get(id=perfil_id)
    # Creates the range bidget filter
    budget_range = [perfil.presupuesto_min, perfil.presupuesto_max]
    # Creates cities list filter
    citites = retrieveProfileCitiesIDs(perfil)
    unspsc = retrieveProfileUNSPSCIDs(perfil)

    if user_request:
        oportunities_match = Oportunidad.objects.select_related().filter(Q(cod_unspsc__in=unspsc) |
                                                        Q(cod_unspsc_familia__in=unspsc) | Q(cod_unspsc_clase__in=unspsc), valor_proceso__range=budget_range,
                                                        municipio_ejecucion__in=citites).order_by('-fecha_publicacion')
    else:        
        oportunities_match = Oportunidad.objects.filter(Q(cod_unspsc__in=unspsc) |
                                                        Q(cod_unspsc_familia__in=unspsc) | Q(cod_unspsc_clase__in=unspsc), valor_proceso__range=budget_range,
                                                        municipio_ejecucion__in=citites).values_list('num_proceso', flat=True)
        oportunities_match = [list(oportunities_match), perfil_id]
    return oportunities_match


def retrieveProfileCitiesIDs(profile):
    cities = []
    for city in profile.ciudad.all():
        cities.append(city.codigo_ciudad)
    return cities


def retrieveProfileUNSPSCIDs(profile):
    unspsc = []
    for activity in profile.activ_economica.all():
        unspsc.append(activity.codigo)
    return unspsc


class NewOportunitiesInfo:
    def __init__(self, initial_data):
        self.oportunities_id, self.profile_id = initial_data
        self.oportunities = None
        self.user = None
        self.user_mail = None

    def getUserData(self):
        user = Perfil.objects.get(id=self.profile_id).usuario
        self.user = user.first_name
        self.user_mail = user.email
        return self.user, self.user_mail

    def getOportunities(self):
        self.oportunities = Oportunidad.objects.filter(num_proceso__in=self.oportunities_id).values_list(
            'detalle_objeto_proceso', 'entidad', 'valor_proceso').order_by('-valor_proceso')
        return self.oportunities
