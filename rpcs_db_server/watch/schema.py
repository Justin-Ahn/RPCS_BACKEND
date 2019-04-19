import graphene
from graphene_django import DjangoObjectType

from .models import Patient, Event
from django.db.models import Q

class PatientType(DjangoObjectType):
	class Meta:
		model = Patient

class EventType(DjangoObjectType):
	class Meta:
		model = Event

class CreatePatient(graphene.Mutation):
    patient_name = graphene.String()
    patient_id = graphene.Int()
    event = graphene.String()
    event_id = graphene.Int()

    class Arguments:
        patient_name = graphene.String()
        patient_id = graphene.Int()
        event = graphene.String()
        event_id = graphene.Int()
    
    def mutate(self, info, patient_name, patient_id, event, event_id):
        user = info.context.user or None

        patient = Patient(patient_name=patient_name, patient_id=patient_id,
            event=event, event_id=event_id)
        patient.save()

        return CreatePatient(
            patient_name = patient.patient_name,
            patient_id = patient.patient_id,
            event = patient.event,
            event_id = patient.event_id
        )


class CreateEvent(graphene.Mutation):
    event_id = graphene.Int()
    event_description = graphene.String()
    event_category = graphene.String()

    class Arguments:
        event_id = graphene.Int()
        event_description = graphene.String()
        event_category = graphene.String()

    def mutate(self, info, event_id, event_description, event_category):
        user = info.context.user or None

        event = Event(event_id=event_id, event_description=event_description,
            event_category=event_category)
        event.save()

        return CreateEvent(
            event_id = event.event_id,
            event_description = event.event_description,
            event_category = event.event_category
        )

class Query(graphene.ObjectType):
    patient = graphene.List(PatientType, id=graphene.Int())
    event = graphene.List(EventType, id=graphene.Int())

    def resolve_patient(self, info, id=-1, **kwargs):
        if id>=0:
            filter = (
                Q(patient_id=id)
            )
            return Patient.objects.filter(filter)    
        
        return Patient.objects.all()
	
    def resolve_event(self, info, id=-1, **kwargs):
        if id>=0:
            filter = (
                Q(event_id=id)
            )
            return Event.objects.filter(filter)
        return Event.objects.all()

class Mutation(graphene.ObjectType):
    create_patient = CreatePatient.Field()
    create_event = CreateEvent.Field()
