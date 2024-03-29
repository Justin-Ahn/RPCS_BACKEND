from django.db import models

# Create your models here.

class PatientProfile(models.Model):
    patient_id = models.IntegerField()
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    medication = models.CharField(max_length=500)
    stage = models.CharField(max_length=200)
    notes = models.CharField(max_length=800)

class CaregiverProfile(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    patient_id = models.IntegerField()
    schedule = models.CharField(max_length=800)
    caregiver_id = models.IntegerField()

class DoctorProfile(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    patient_id = models.IntegerField()
    appointment = models.CharField(max_length=800)
    doctor_id = models.IntegerField()
