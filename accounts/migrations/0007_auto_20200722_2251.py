# Generated by Django 3.0.8 on 2020-07-23 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200711_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudad',
            name='id',
        ),
        migrations.AddField(
            model_name='ciudad',
            name='codigo_ciudad',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]