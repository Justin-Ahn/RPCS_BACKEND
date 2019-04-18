from django.db import models

# Create your models here.
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
    num_injuries = models.IntegerField()
    num_falls = models.IntegerField()
    weight = models.FloatField()
    body_fat_percentage = models.FloatField()
