import graphene
from graphene_django import DjangoObjectType

from .models import Patient, Caregiver, Safezone
from django.db.models import Q

class WtPatientType(DjangoObjectType):
	class Meta:
		model = Patient

class WtCaregiverType(DjangoObjectType):
    class Meta:
        model = Caregiver

class SafezoneType(DjangoObjectType):
    class Meta:
        model = Safezone

class CreateWtPatient(graphene.Mutation):
    location = graphene.String()
    timestamp = graphene.types.datetime.DateTime()
    patient_id = graphene.Int()
    wt_patient_id = graphene.Int()

    class Arguments:
        location = graphene.String()
        timestamp = graphene.types.datetime.DateTime()
        patient_id = graphene.Int()
        wt_patient_id = graphene.Int()

    def mutate(self, info, location, timestamp, patient_id, wt_patient_id):
        user = info.context.user or None

        pt = Patient(location=location, timestamp=timestamp,
            patient_id=patient_id, wt_patient_id=wt_patient_id)
        pt.save()

        return CreateWtPatient(
            location = pt.location,
            timestamp = pt.timestamp,
            patient_id = pt.patient_id,
            wt_patient_id = wt_patient_id
        )

class CreateWtCaregiver(graphene.Mutation):
    location = graphene.String()
    timestamp = graphene.types.datetime.DateTime()
    caregiver_id = graphene.Int()
    wt_caregiver_id = graphene.Int()

    class Arguments:
        location = graphene.String()
        timestamp = graphene.types.datetime.DateTime()
        caregiver_id = graphene.Int()
        wt_caregiver_id = graphene.Int()

    def mutate(self, info, location, timestamp, caregiver_id, wt_caregiver_id):
        user = info.context.user or None

        cg = Caregiver(location=location, timestamp=timestamp,
            caregiver_id=caregiver_id, wt_caregiver_id=wt_caregiver_id)
        cg.save()

        return CreateWtCaregiver(
            location = cg.location,
            timestamp = cg.timestamp,
            caregiver_id = cg.caregiver_id,
            wt_caregiver_id = cg.wt_caregiver_id
        )

class CreateSafezone(graphene.Mutation):
    location = graphene.String()
    radius = graphene.Float()
    patient_id = graphene.Int()
    wt_safezone_id = graphene.Int()

    class Arguments:
        location = graphene.String()
        radius = graphene.Float()
        patient_id = graphene.Int()
        wt_safezone_id = graphene.Int()

    def mutate(self, info, location, radius, patient_id, wt_safezone_id):
        user = info.context.user or None

        sz = Safezone(location=location, radius=radius, patient_id=patient_id,
            wt_safezone_id=wt_safezone_id)
        sz.save()

        return CreateSafezone(
            location = sz.location,
            radius = sz.radius,
            patient_id = sz.patient_id,
            wt_safezone_id = sz.wt_safezone_id
        )

class Query(graphene.ObjectType):
    wt_patient = graphene.List(WtPatientType, id = graphene.Int())
    wt_caregiver = graphene.List(WtCaregiverType, id = graphene.Int())
    safezone = graphene.List(SafezoneType, id = graphene.Int())

    def resolve_wt_patient(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(wt_patient_id=id)
            )
            return Patient.objects.filter(filter)
        return Patient.objects.all()

    def resolve_wt_caregiver(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(wt_caregiver_id=id)
            )
            return Caregiver.objects.filter(filter)
        return Caregiver.objects.all()

    def resolve_safezone(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(wt_safezone_id=id)
            )
            return Safezone.objects.filter(filter)
        return Safezone.objects.all()
	
class Mutation(graphene.ObjectType):
    create_wt_patient = CreateWtPatient.Field()
    create_wt_caregiver = CreateWtCaregiver.Field()
    create_safezone = CreateSafezone.Field()
