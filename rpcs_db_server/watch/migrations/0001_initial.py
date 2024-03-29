# Generated by Django 2.1.7 on 2019-04-10 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(default=0)),
                ('event_description', models.TextField(blank=True)),
                ('event_category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=50)),
                ('patient_id', models.IntegerField(default=0)),
                ('event', models.CharField(max_length=100)),
                ('event_id', models.IntegerField(default=0)),
            ],
        ),
    ]
