from .tasks import addRemoveFavsTask

# Django
from django.shortcuts import render

# Utilities
from oportunities.utilities.match_oportunities import matchOportunities, retrivefavoritesUser

# Models
from subscriptions.models import Subscription

# Create your views here.

def user_oportunities(request):
    subscriptions = Subscription.objects.filter(user=request.user.id, active=True).values("plan")
    # Check if the user has had plans
    if subscriptions.count() == 0:
        title = "Usted no cuenta con una suscripción activa"
        message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
        detail = "Estaremos atentos a sus inquietudes y sugerencias."
        return render(
            request,
            "subscriptions/registered_subscription_plans.html",
            {"title": title, "message": message, "detail": detail},
        )

    oportunities = matchOportunities(request.user.perfil.id, True)
    favorites = retrivefavoritesUser(request.user.perfil.id)
    if len(oportunities) != 0:
        return render(request, 'oportunities/user_oportunities.html', 
                        {'oportunities': oportunities, 'favorites': favorites})
    else:
        return render(request, 'oportunities/user_oportunities_empty.html')
        

def user_oportunities_favs(request):
    subscriptions = Subscription.objects.filter(user=request.user.id, active=True).values("plan")
    # Check if the user has had plans
    if subscriptions.count() == 0:
        title = "Usted no cuenta con una suscripción activa"
        message = "Adquiera el plan que más se ajuste a las necesidades de su empresa."
        detail = "Estaremos atentos a sus inquietudes y sugerencias."
        return render(
            request,
            "subscriptions/registered_subscription_plans.html",
            {"title": title, "message": message, "detail": detail},
        )

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
