# Generated by Django 2.1.5 on 2019-04-08 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_emailrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
