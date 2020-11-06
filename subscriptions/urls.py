"""Subscription urls."""

# Django
from django.urls import path

# Views
from subscriptions.views import subscription_validate, payment_response

urlpatterns = [
    path('validate/', subscription_validate, name='subscription_validate'),
    path('payment/', payment_response, name='payment'),
]
