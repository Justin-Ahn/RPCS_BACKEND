from django.db import models

# Create your models here.
class Event(models.Model):
    event_type = models.CharField()
    sensor_id = models.UUIDField()
    sensor_type = models.CharField()
    timestamp = models.DateTimeField()
    data = models.BinaryField()
    event_id = models.IntegerField()