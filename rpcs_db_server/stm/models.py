from django.db import models

class Results(models.Model):  
    patient_name = models.CharField(max_length=50)
    patient_id = models.IntegerField(default=0)
    scaled_rating1 = models.IntegerField(default=0)
    scaled_rating2 = models.IntegerField(default=0)
    test_Results = models.TextField(blank=True)



# Create your models here.
