from django.db import models

# Create your models here.

class Patient(models.Model):
    location = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    patient_id = models.IntegerField(default=0)
    wt_patient_id = models.AutoField(primary_key=True)
    

class Caregiver(models.Model):
    location = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    caregiver_id = models.IntegerField(default=0)
    wt_caregiver_id = models.AutoField(primary_key=True)


class Safezone(models.Model):
    location = models.CharField(max_length=500)
    radius = models.FloatField(null=True, blank=True, default=None)
    patient_id = models.IntegerField(default=0)
    wt_safezone_id = models.AutoField(primary_key=True)

