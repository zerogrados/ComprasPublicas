from django.db import models
from accounts.models import CodUNSPSC, Ciudad
from datetime import datetime
# Create your models here.

class Oportunidad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    num_proceso = models.CharField(verbose_name='numero_proceso', max_length=50)
    cod_unspsc = models.ForeignKey(CodUNSPSC, related_name='codigo_unspsc', on_delete=models.SET_NULL, null=True)
    cod_unspsc_adicionales = models.ManyToManyField(CodUNSPSC, related_name='codigos_adicionales')
    cod_unspsc_familia = models.ForeignKey(CodUNSPSC, on_delete=models.SET_NULL, related_name='codigo_familia', null=True, blank=True)
    cod_unspsc_clase = models.ForeignKey(CodUNSPSC, on_delete=models.SET_NULL, related_name='codigo_clase', null=True, blank=True)
    estado_proceso = models.CharField(verbose_name='estado', max_length=15)
    fuente = models.IntegerField(verbose_name='fuente_informacion')
    entidad = models.CharField(verbose_name='entidad_contratante', max_length=200, null=True, blank=True)
    municipio_entidad = models.ForeignKey(Ciudad, verbose_name='municipio_entidad', on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_entidad')
    nit_entidad = models.CharField(verbose_name='nit_entidad', max_length=20, null=True, blank=True)
    objeto_proceso = models.TextField(verbose_name='objeto_proceso', max_length=500, null=True, blank=True)
    detalle_objeto_proceso = models.TextField(verbose_name='detalle_objeto_proceso', max_length=1000, null=True, blank=True)
    valor_proceso = models.DecimalField(verbose_name='valor_proceso', max_digits=52, decimal_places=2, null=True)
    id_tipo_proceso = models.IntegerField(verbose_name='id_tipo_proceso', null=True, blank=True)
    tipo_proceso = models.CharField(verbose_name='tipo_proceso', max_length=150, null=True, blank=True)
    fecha_publicacion = models.DateField(verbose_name='fecha_publicacion', null=True, blank=True)
    plazo_ejecucion_cant = models.IntegerField(verbose_name='plazo_ejecucion_cantidad', null=True, blank=True)
    plazo_ejecucion_und = models.CharField(verbose_name='plazo_ejecucion_unidad', max_length=5, null=True, blank=True)
    municipio_ejecucion = models.ForeignKey(Ciudad, verbose_name='municipio_ejecucion', on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_ejecucion')
    municipio_ejecucion_adicional = models.ManyToManyField(Ciudad, related_name='municipio_ejecucion_adicional')
    fecha_limite = models.DateField(verbose_name='fecha_limite', null=True, blank=True)
    url_proceso = models.URLField(verbose_name='url_proceso', null=True, blank=True, max_length=255)
    undefined_flag = models.BooleanField(verbose_name='undefined', default=False)

    def __str__(self):
        return str(self.num_proceso)
    