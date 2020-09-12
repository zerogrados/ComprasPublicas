
# Django
from django.urls import include, path
# Views
from oportunities.views import user_oportunities, user_oportunities_favs, addRemoveFavs

urlpatterns = [
    path('me/', user_oportunities, name='user_oportunities'),
    path('favs/', user_oportunities_favs, name='user_oportunities_favs'),
    path('fav/<str:processId>/<int:state>', addRemoveFavs, name='addRemoveFavs'),
]
