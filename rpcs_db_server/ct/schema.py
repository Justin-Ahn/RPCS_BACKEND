import graphene
from graphene_django import DjangoObjectType

from .models import Incident, Trend
from django.db.models import Q

class IncidentType(DjangoObjectType):
    class Meta:
        model = Incident

class TrendType(DjangoObjectType):
    class Meta:
        model = Trend

class CreateIncident(graphene.Mutation):
    patient_id = graphene.Int()
    incident_id = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()
    pulse_rate = graphene.Float()
    respiratory_rate = graphene.Float()
    blood_pressure = graphene.Float()
    incident_type = graphene.String()
    recording = graphene.String()
    details = graphene.String()

    class Arguments:
        patient_id = graphene.Int()
        incident_id = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()
        pulse_rate = graphene.Float()
        respiratory_rate = graphene.Float()
        blood_pressure = graphene.Float()
        incident_type = graphene.String()
        recording = graphene.String()
        details = graphene.String()

    def mutate(self, info, patient_id, incident_id, timestamp, pulse_rate,
        respiratory_rate, blood_pressure, incident_type, recording, details):

        user = info.context.user or None

        inc = Incident(patient_id=patient_id, incident_id=incident_id,
            timestamp=timestamp, pulse_rate=pulse_rate, 
            respiratory_rate=respiratory_rate, blood_pressure=blood_pressure,
            incident_type=incident_type, recording=recording, details=details)
        inc.save()

        return CreateIncident(
            patient_id = inc.patient_id,
            incident_id = inc.incident_id,
            timestamp = inc.timestamp, 
            pulse_rate = inc.pulse_rate, 
            respiratory_rate = inc.respiratory_rate, 
            blood_pressure = inc.blood_pressure,
            incident_type = inc.incident_type, 
            recording = inc.recording,
            details = inc.details
        )

class CreateTrend(graphene.Mutation):
    patient_id = graphene.Int()
    test_score = graphene.Int()
    num_injuries = graphene.Int()
    num_falls = graphene.Int()
    weight = graphene.Float()
    body_fat_percentage = graphene.Float()

    class Arguments:
        patient_id = graphene.Int()
        test_score = graphene.Int()
        num_injuries = graphene.Int()
        num_falls = graphene.Int()
        weight = graphene.Float()
        body_fat_percentage = graphene.Float()

    def mutate(self, info, patient_id, test_score, num_injuries, num_falls,
        weight, body_fat_percentage):
        user = info.context.user or None

        trend = Trend(patient_id=patient_id, test_score=test_score, 
            num_injuries=num_injuries, num_falls=num_falls,
            weight=weight, body_fat_percentage=body_fat_percentage)
        trend.save()

        return CreateTrend(
            patient_id = trend.patient_id, 
            test_score = trend.test_score, 
            num_injuries = trend.num_injuries, 
            num_falls = trend.num_falls,
            weight = trend.weight, 
            body_fat_percentage = trend.body_fat_percentage
        )

class Query(graphene.ObjectType):
    incident = graphene.List(IncidentType, id = graphene.Int())
    trend = graphene.List(TrendType, id = graphene.Int())

    def resolve_incident(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Incident.objects.filter(filter)
        return Incident.objects.all()

    def resolve_trend(self, info, id=-1, **kwargs):
        if id>=0:
            filter = (
                Q(patient_id=id)
            )
            return Trend.objects.filter(filter)
            
        return Trend.objects.all()

class Mutation(graphene.ObjectType):
    create_incident = CreateIncident.Field()
    create_trend = CreateTrend.Field()

