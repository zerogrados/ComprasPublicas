"""Subscription urls."""

# Django
from django.urls import path

# Views
from subscriptions.views import subscription_validate

urlpatterns = [
    path('validate/', subscription_validate, name='subscription_validate'),
]
