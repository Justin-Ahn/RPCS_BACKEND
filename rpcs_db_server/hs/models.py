from django.db import models

# Create your models here.
class Events(models.Model):
    event_type = models.CharField(max_length=200)
    sensor_id = models.UUIDField()
    sensor_type = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    data = models.CharField(max_length=5000)
    event_id = models.AutoField(primary_key=True)
