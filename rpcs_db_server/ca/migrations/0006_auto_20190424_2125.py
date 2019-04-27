# Generated by Django 2.2 on 2019-04-24 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0005_auto_20190416_2327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident_summary',
            old_name='num_injury',
            new_name='num_falls',
        ),
        migrations.RemoveField(
            model_name='incident_summary',
            name='num_hallucinations',
        ),
        migrations.RemoveField(
            model_name='sleep_trend',
            name='hours_deep_sleep',
        ),
        migrations.RemoveField(
            model_name='sleep_trend',
            name='hours_light_sleep',
        ),
    ]