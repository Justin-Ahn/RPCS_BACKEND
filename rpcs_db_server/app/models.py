from django.db import models

# Create your models here.
# class WtPaitent(models.Model):
#     location = models.CharField()
#     timestamp = models.DateTimeField(auto_now_add=True)
    
# class WtCaregiver(models.Model):
#     location = models.CharField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# class WtSafezone(models.Model):
#     location = models.CharField()
#     radius = models.IntegerField()
#     patient = models.ForeignKey(WtPaitent, on_delete=models.CASCADE)
#     