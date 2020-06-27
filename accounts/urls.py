from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('registro/', views.creaUsuarioView, name='registro'),
    path('cerrar_sesion/', views.logoutView, name='cerrar_sesion')
]