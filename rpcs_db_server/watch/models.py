from django.db import models

# Create your models here.

class Patient(models.Model):
    patient_name = models.CharField(max_length=50)
    patient_id = models.IntegerField(default=0)
    event = models.CharField(max_length=100)
    event_id = models.IntegerField(default=0)


class Event(models.Model):
    event_id = models.IntegerField(default=0)
    event_description = models.TextField(blank=True)
    event_category = models.CharField(max_length=100)


