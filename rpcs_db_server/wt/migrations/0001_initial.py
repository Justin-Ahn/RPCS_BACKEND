# Generated by Django 2.1.7 on 2019-04-10 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caregiver',
            fields=[
                ('location', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('caregiver_id', models.IntegerField(default=0)),
                ('wt_caregiver_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('location', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient_id', models.IntegerField(default=0)),
                ('wt_patient_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Safezone',
            fields=[
                ('location', models.CharField(max_length=500)),
                ('radius', models.FloatField(blank=True, default=None, null=True)),
                ('patient_id', models.IntegerField(default=0)),
                ('wt_safezone_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
