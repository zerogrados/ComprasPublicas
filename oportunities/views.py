from .tasks import addRemoveFavsTask

# Django
from django.shortcuts import render, redirect

# Utilities
from oportunities.utilities.match_oportunities import matchOportunities, retrivefavoritesUser


# Create your views here.

def user_oportunities(request):
    oportunities = matchOportunities(request.user.perfil.id, True)
    favorites = retrivefavoritesUser(request.user.perfil.id)
    return render(request, 'oportunities/user_oportunities.html', 
                    {'oportunities': oportunities, 'favorites': favorites})

def user_oportunities_favs(request):
    oportunities = matchOportunities(request.user.perfil.id, True)
    favorites = retrivefavoritesUser(request.user.perfil.id)
    return render(request, 'oportunities/user_oportunities_favs.html', 
                    {'oportunities': oportunities, 'favorites': favorites})

def addRemoveFavs(request, processId=None, state=0):
    addRemoveFavsTask.delay(request.user.id, processId, state)
    pass
