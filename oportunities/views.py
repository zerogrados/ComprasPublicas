from .tasks import addRemoveFavsTask

# Django
from django.shortcuts import render

# Utilities
from oportunities.utilities.match_oportunities import matchOportunities


# Create your views here.

def user_oportunities(request):
    oportunities = matchOportunities(request.user.perfil.id, True)
    return render(request, 'oportunities/user_oportunities.html', {'oportunities': oportunities})


def addRemoveFavs(request, num_proceso=None, state=0):
    addRemoveFavsTask.delay(self.request.user.id, num_proceso, state)
    return render(request, 'oportunities/user_oportunities.html', {'oportunities': oportunities})
