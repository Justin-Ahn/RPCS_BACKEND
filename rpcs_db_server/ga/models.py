from django.db import models

# Create your models here.
class Logical(models.Model):
    patient_id = models.IntegerField()
    logical_thinking_score = models.IntegerField()
    timestamp = models.DateTimeField()

class Semantic(models.Model):
    patient_id = models.IntegerField()
    semantic_score = models.IntegerField()
    timestamp = models.DateTimeField()

class Procedual(models.Model):
    patient_id = models.IntegerField()
    procedural_score = models.IntegerField()
    timestamp = models.DateTimeField()

class Episodic(models.Model):
    patient_id = models.IntegerField()
    episodic_score = models.IntegerField()
    timestamp = models.DateTimeField()
    question = models.CharField()
    answer_choices = models.CharField()
    patient_answer = models.CharField()
    correct_answer = models.CharField()
