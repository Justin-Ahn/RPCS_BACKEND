# Generated by Django 2.2 on 2019-04-19 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('int', '0002_auto_20190418_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiverprofile',
            name='schedule',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='appointment',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='doctor',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='medication',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='notes',
            field=models.CharField(max_length=800),
        ),
    ]
