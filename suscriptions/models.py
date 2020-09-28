"""Suscription models."""

# Django
from django.db import models

# Models
from accounts.models import Usuario

# Create your models here.

class Plan(models.Model):
    """Plan model."""
    name = models.CharField(null=False, blank=False, max_length=100)
    months = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    offer = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Suscription(models.Model):
    """Suscription model."""
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
