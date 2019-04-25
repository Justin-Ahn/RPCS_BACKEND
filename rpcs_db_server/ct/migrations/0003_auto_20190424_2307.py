# Generated by Django 2.2 on 2019-04-24 23:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0002_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='blood_pressure',
        ),
        migrations.AddField(
            model_name='incident',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='incident',
            name='pulse_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='respiratory_rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
