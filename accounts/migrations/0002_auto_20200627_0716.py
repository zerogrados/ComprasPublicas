# Generated by Django 3.0.7 on 2020-06-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='nit',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nom_empresa',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='presupuesto_max',
            field=models.DecimalField(decimal_places=2, max_digits=52, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='presupuesto_min',
            field=models.DecimalField(decimal_places=2, max_digits=52, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
