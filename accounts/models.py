from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Usuario(AbstractUser):

    tipo_documento = models.CharField(null=True, blank=True, max_length=3)
    num_documento = models.CharField(null=True, blank=True, max_length=20)
    modified_at = models.DateTimeField(auto_now=True)
    celular = PhoneNumberField(null=False, blank=False, region='CO')

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.last_name + ' - ' + self.num_documento


class CodUNSPSC(models.Model):
    # Modelo para almacenar los codigos de las actividades economicas
    codigo = models.CharField(null=False, blank=False, max_length=10)


class Ciudad(models.Model):
    # Modelo para almacenar ciudades de operacion
    ciudad = models.CharField(null=False, blank=False, max_length=20)


class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nit = models.CharField(max_length=15, null=True)
    nom_empresa = models.CharField(max_length=150, null=True)
    telefono = models.CharField(max_length=30, null=True)
    activ_economica = models.ManyToManyField(
        CodUNSPSC, related_name='actividades_economicas')
    presupuesto_min = models.DecimalField(
        max_digits=52, decimal_places=2, null=True)
    presupuesto_max = models.DecimalField(
        max_digits=52, decimal_places=2, null=True)
    ciudad = models.ManyToManyField(Ciudad, related_name='ciudades')
