from django.db import models

# Create your models here.
class Logical(models.Model):
    patient_id = models.IntegerField()
    logical_score = models.IntegerField()
    timestamp = models.DateTimeField()
    game_id = models.IntegerField(default=0)

class Semantic(models.Model):
    patient_id = models.IntegerField()
    semantic_score = models.IntegerField()
    timestamp = models.DateTimeField()

class Procedural(models.Model):
    patient_id = models.IntegerField()
    procedural_score = models.IntegerField()
    timestamp = models.DateTimeField()

class Episodic(models.Model):
    patient_id = models.IntegerField()
    episodic_score = models.IntegerField()
    timestamp = models.DateTimeField()
    question = models.CharField(max_length=200)
    answer_choices = models.CharField(max_length=200)
    patient_answer = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
