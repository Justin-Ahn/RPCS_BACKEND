from django.db import models

# Create your models here.
class Wandering(models.Model):
    patient_id = models.IntegerField()
    caregiver_id = models.IntegerField()
    isWandering = models.BooleanField()
    alerted = models.BooleanField()


class Phys_measure(models.Model):
    patient_id = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=200)
    stage = models.CharField(max_length=200)
    weight = models.FloatField()
    body_fat = models.FloatField()
    skinny_fat = models.FloatField()
    bp_low = models.IntegerField()
    bp_high = models.IntegerField()
    pr_low = models.IntegerField()
    pr_high = models.IntegerField()
    rr_low = models.IntegerField()
    rr_high = models.IntegerField()

class Phys_params(models.Model):
    patient_id = models.IntegerField()
    coef_bp = models.FloatField()
    coef_pr = models.FloatField()
    coef_rr = models.FloatField()
    bias_logit = models.FloatField()
    ar = models.FloatField()

class Phys_incidents(models.Model):
    patient_id = models.IntegerField()
    incident_id = models.IntegerField()
    timestamp = models.DateTimeField()
    pulse_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    blood_pressure = models.FloatField()
    incident_type = models.CharField(max_length=200)
    recording = models.CharField(max_length=200)

class Sleep_trend(models.Model):
    patient_id = models.IntegerField()
    date = models.DateField()
    hours_slept = models.FloatField(blank=True, null=True)
    hours_in_bed = models.FloatField(blank=True, null=True)
    num_wake_up = models.IntegerField(blank=True, null=True)
    num_get_out_of_bed = models.IntegerField(blank=True, null=True)
    num_go_to_bathroom = models.IntegerField(blank=True, null=True)

class Incident_summary(models.Model):
    patient_id = models.IntegerField()
    date = models.DateField()
    num_ltm_lapse = models.IntegerField(blank=True, null=True)
    num_stm_lapse = models.IntegerField(blank=True, null=True)
    num_falls = models.IntegerField(blank=True, null=True)
    num_wandering = models.IntegerField(blank=True, null=True)
