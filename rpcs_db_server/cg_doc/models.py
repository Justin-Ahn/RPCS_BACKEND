from django.db import models

# Create your models here.

class CaregiverProfile(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    patient_id = models.IntegerField()
    schedule = models.CharField(max_length=200)

class DoctorProfile(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    patient_id = models.IntegerField()
    appointment = models.CharField(max_length=200)
