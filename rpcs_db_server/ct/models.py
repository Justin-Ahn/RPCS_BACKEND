from django.db import models

# Create your models here.

class Profile(models.Model):
    patient_id = models.IntegerField()
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=200)
    doctor = models.IntegerField()
    medication = models.CharField(max_length=200)
    stage = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)

class Incident(models.Model):
    patient_id = models.IntegerField()
    incident_id = models.IntegerField()
    timestamp = models.DateTimeField()
    pulse_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    blood_pressure = models.FloatField()
    incident_type = models.CharField(max_length=200)
    recording = models.CharField(max_length=200)

class Trend(models.Model):
    patient_id = models.IntegerField()
    test_score = models.IntegerField()
    num_injuries = num_falls = models.IntegerField()
    weight = models.FloatField()
    body_fat_percentage = models.FloatField()