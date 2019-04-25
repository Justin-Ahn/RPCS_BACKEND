import graphene
from graphene_django import DjangoObjectType

from .models import CaregiverProfile, DoctorProfile
from django.db.models import Q

class CaregiverProfileType(DjangoObjectType):
	class Meta:
		model = CaregiverProfile

class DoctorProfileType(DjangoObjectType):
    class Meta:
        model = DoctorProfile

class CreateCaregiverProfile(graphene.Mutation):
    name = graphene.String()
    username = graphene.String()
    password = graphene.String()
    patient_id = graphene.Int()
    schedule = graphene.String()

    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        patient_id = graphene.Int()
        schedule = graphene.String()

    def mutate(self, info, name, username, password, patient_id, schedule):
        user = info.context.user or None

        cg_profile = CaregiverProfile(name=name, username=username,
            password=password, patient_id=patient_id, schedule=schedule)
        cg_profile.save()

        return CreateCaregiverProfile(
            name = name,
            username = username,
            password = password,
            patient_id = patient_id,
            schedule = schedule)

class CreateDoctorProfile(graphene.Mutation):
    name = graphene.String()
    username = graphene.String()
    password = graphene.String()
    patient_id = graphene.Int()
    appointment = graphene.String()

    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        patient_id = graphene.Int()
        appointment = graphene.String()

    def mutate(self, info, name, username, password, patient_id, appointment):
        user = info.context.user or None
        
        doc_profile = DoctorProfile(name=name, username=username,
            password=password, patient_id=patient_id, appointment=appointment)
        doc_profile.save()

        return CreateDoctorProfile(
            name = name,
            username = username,
            password = password,
            patient_id = patient_id,
            appointment = appointment)

class Query(graphene.ObjectType):
	#results = graphene.List(StmType, id = graphene.Int())
    caregiver_profile = graphene.List(CaregiverProfileType)
    doctor_profile = graphene.List(DoctorProfileType)
	
    def resolve_caregiver_profile(self, info, **kwargs):
        return CaregiverProfile.objects.all()

    def resolve_doctor_profile(self, info, **kwargs):
        return DoctorProfile.objects.all()

	#def resolve_results(self, info, id=-1, **kwargs):
	#if id>=0:
	#filter = (
	#    Q(patient_id=id)
	#		)
	#		return Results.objects.filter(filter)

	#	return Results.objects.all()

class Mutation(graphene.ObjectType):
    create_caregiver_profile = CreateCaregiverProfile.Field()
    create_doctor_profile = CreateDoctorProfile.Field()
