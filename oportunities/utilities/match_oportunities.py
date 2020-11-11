from oportunities.models import Oportunidad, Favorito
from accounts.models import Perfil
from django.db.models import Q
import datetime

def matchOportunities(perfil_id, user_request=None):
    perfil = Perfil.objects.get(id=perfil_id)
    # Creates the range bidget filter
    budget_range = [perfil.presupuesto_min, perfil.presupuesto_max]
    # Creates cities list filter
    citites = retrieveProfileCitiesIDs(perfil)
    unspsc = retrieveProfileUNSPSCIDs(perfil)

    date = datetime.datetime.today() - datetime.timedelta(days=31)
    oportunities_fav = Favorito.objects.filter(~Q(usuario_id=1)).values_list("oportunidad_id", flat=True)

    if user_request:
        oportunities_match = Oportunidad.objects.select_related().filter(Q(cod_unspsc__in=unspsc) |
                                                        Q(cod_unspsc_familia__in=unspsc) | Q(cod_unspsc_clase__in=unspsc), valor_proceso__range=budget_range,
                                                        municipio_ejecucion__in=citites).order_by('-fecha_publicacion')
        oportunities_match = oportunities_match.filter(~(Q(estado_proceso="Adjudicado") & Q(fecha_publicacion__lte=date) & Q(id__in=oportunities_fav)))
        oportunities_match = oportunities_match.filter(~(Q(estado_proceso="Celebrado") & Q(fecha_publicacion__lte=date) & Q(id__in=oportunities_fav)))
    else:        
        oportunities_match = Oportunidad.objects.filter(Q(cod_unspsc__in=unspsc) |
                                                        Q(cod_unspsc_familia__in=unspsc) | Q(cod_unspsc_clase__in=unspsc), valor_proceso__range=budget_range,
                                                        municipio_ejecucion__in=citites).values_list('num_proceso', flat=True)
        oportunities_match = oportunities_match.filter(~(Q(estado_proceso="Adjudicado") & Q(fecha_publicacion__lte=date) & Q(id__in=oportunities_fav)))
        oportunities_match = oportunities_match.filter(~(Q(estado_proceso="Celebrado") & Q(fecha_publicacion__lte=date) & Q(id__in=oportunities_fav)))                                                        
        oportunities_match = [list(oportunities_match), perfil_id]

    return oportunities_match


def retrieveProfileCitiesIDs(profile):
    cities = []
    for city in profile.ciudades.all():
        cities.append(city.codigo_ciudad)
    return cities


def retrieveProfileUNSPSCIDs(profile):
    unspsc = []
    for activity in profile.activ_economica.all():
        unspsc.append(activity.codigo)
    return unspsc

def retrivefavoritesUser(user_id):
    favorites = Favorito.objects.filter(usuario_id=user_id).values_list('oportunidad_id', flat=True)
    return favorites

class NewOportunitiesInfo:
    def __init__(self, initial_data):
        self.oportunities_id, self.profile_id = initial_data
        self.oportunities = None
        self.user = None
        self.user_mail = None

    def getUserData(self):
        user = Perfil.objects.filter(id=self.profile_id).prefetch_related('usuario').values('usuario__first_name', 'usuario__email')
        self.user = user[0]['usuario__first_name']
        self.user_mail = user[0]['usuario__email']
        return self.user, self.user_mail

    def getOportunities(self):
        self.oportunities = Oportunidad.objects.filter(num_proceso__in=self.oportunities_id).values_list(
            'detalle_objeto_proceso', 'entidad', 'valor_proceso').order_by('-valor_proceso')
        return self.oportunities
