
# Django
from django.urls import include, path
# Views
from oportunities.views import user_oportunities

urlpatterns = [
    path('my-oportunities', user_oportunities, name='user_oportunities'),
]
