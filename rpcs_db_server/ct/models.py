from django.db import models

# Create your models here.

class Trend(models.Model):
    patient_id = models.IntegerField()
    test_score = models.IntegerField()
    num_injuries = models.IntegerField()
    num_falls = models.IntegerField()
    weight = models.FloatField()
    body_fat_percentage = models.FloatField()
