"""Suscription urls."""

# Django
from django.urls import path

# Views
from suscriptions.views import suscription_validate

urlpatterns = [
    path('validate/', suscription_validate, name='suscription_validate'),
]
