from django.db import models
import datetime

# Create your models here.
class Incident(models.Model):
    patient_id = models.IntegerField()
    incident_id = models.IntegerField()
    timestamp = models.DateTimeField()
    date = models.DateField(default=datetime.date.today)
    pulse_rate = models.FloatField(null=True, blank=True)
    respiratory_rate = models.FloatField(null=True, blank=True)
    incident_type = models.CharField(max_length=200)
    recording = models.CharField(max_length=200)
    details = models.CharField(max_length=1000)

class Trend(models.Model):
    patient_id = models.IntegerField()
    test_score = models.IntegerField()
    num_injuries = models.IntegerField()
    num_falls = models.IntegerField()
    weight = models.FloatField()
    body_fat_percentage = models.FloatField()
