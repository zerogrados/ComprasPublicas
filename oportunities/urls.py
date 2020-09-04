
# Django
from django.urls import include, path
# Views
from oportunities.views import user_oportunities, addRemoveFavs

urlpatterns = [
    path('my-oportunities', user_oportunities, name='user_oportunities'),
    path('fav/<str:processId>/<int:state>', addRemoveFavs, name='addRemoveFavs'),
]
