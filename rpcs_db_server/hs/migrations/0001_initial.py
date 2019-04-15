# Generated by Django 2.1.7 on 2019-04-11 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=200)),
                ('sensor_id', models.UUIDField()),
                ('sensor_type', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('data', models.BinaryField()),
                ('event_id', models.IntegerField()),
            ],
        ),
    ]