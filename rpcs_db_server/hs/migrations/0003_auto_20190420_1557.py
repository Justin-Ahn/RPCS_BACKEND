# Generated by Django 2.2 on 2019-04-20 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0002_auto_20190415_0351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='id',
        ),
        migrations.AlterField(
            model_name='events',
            name='event_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
