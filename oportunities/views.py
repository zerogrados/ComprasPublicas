from .tasks import addRemoveFavsTask

# Django
from django.shortcuts import render, redirect

# Utilities
from oportunities.utilities.match_oportunities import matchOportunities, retrivefavoritesUser


# Create your views here.

def user_oportunities(request):
    oportunities = matchOportunities(request.user.perfil.id, True)
    favorites = retrivefavoritesUser(request.user.perfil.id)
    if len(favorites) != 0:
        return render(request, 'oportunities/user_oportunities.html', 
                        {'oportunities': oportunities, 'favorites': favorites})
    else:
        return render(request, 'oportunities/user_oportunities_empty.html')
        

def user_oportunities_favs(request):
    oportunities = matchOportunities(request.user.perfil.id, True)
    favorites = retrivefavoritesUser(request.user.perfil.id)
    if len(favorites) != 0:
        return render(request, 'oportunities/user_oportunities_favs.html', 
                    {'oportunities': oportunities, 'favorites': favorites})
    else:
        return render(request, 'oportunities/user_oportunities_favs_empty.html')

def addRemoveFavs(request, processId=None, state=0):
    addRemoveFavsTask.delay(request.user.id, processId, state)
    pass
