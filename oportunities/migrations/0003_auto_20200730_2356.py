# Generated by Django 3.0.8 on 2020-07-31 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oportunities', '0002_auto_20200730_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oportunidad',
            name='entidad',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='entidad_contratante'),
        ),
        migrations.AlterField(
            model_name='oportunidad',
            name='nit_entidad',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='nit_entidad'),
        ),
    ]
