import graphene
from graphene_django import DjangoObjectType

from .models import CaregiverProfile, DoctorProfile, PatientProfile
from django.db.models import Q


class CaregiverProfileType(DjangoObjectType):
	class Meta:
		model = CaregiverProfile


class DoctorProfileType(DjangoObjectType):
    class Meta:
        model = DoctorProfile


class PatientProfileType(DjangoObjectType):
    class Meta:
        model = PatientProfile


class CreateCaregiverProfile(graphene.Mutation):
    name = graphene.String()
    username = graphene.String()
    password = graphene.String()
    patient_id = graphene.Int()
    schedule = graphene.String()
    caregiver_id = graphene.Int()

    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        patient_id = graphene.Int()
        schedule = graphene.String()
        caregiver_id = graphene.Int()

    def mutate(self, info, name, username, password, patient_id, schedule, caregiver_id):
        user = info.context.user or None

        cg_profile = CaregiverProfile(name=name, username=username,
            password=password, patient_id=patient_id, schedule=schedule, caregiver_id=caregiver_id)
        cg_profile.save()

        return CreateCaregiverProfile(
            name = name,
            username = username,
            password = password,
            patient_id = patient_id,
            schedule = schedule,
            caregiver_id = caregiver_id)

class CreateDoctorProfile(graphene.Mutation):
    name = graphene.String()
    username = graphene.String()
    password = graphene.String()
    patient_id = graphene.Int()
    appointment = graphene.String()
    doctor_id = graphene.Int()

    class Arguments:
        name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        patient_id = graphene.Int()
        appointment = graphene.String()
        doctor_id = graphene.Int()

    def mutate(self, info, name, username, password, patient_id, appointment, doctor_id):
        user = info.context.user or None
        
        doc_profile = DoctorProfile(name=name, username=username,
            password=password, patient_id=patient_id, appointment=appointment, doctor_id=doctor_id)
        doc_profile.save()

        return CreateDoctorProfile(
            name = name,
            username = username,
            password = password,
            patient_id = patient_id,
            appointment = appointment,
            doctor_id = doctor_id)

class CreatePatientProfile(graphene.Mutation):
    patient_id = graphene.Int()
    name_ = graphene.String()
    age = graphene.Int()
    gender = graphene.String()
    doctor = graphene.Int()
    medication = graphene.String()
    stage = graphene.String()
    notes = graphene.String()

    class Arguments:
        patient_id = graphene.Int()
        name_ = graphene.String()
        age = graphene.Int()
        gender = graphene.String()
        doctor = graphene.Int()
        medication = graphene.String()
        stage = graphene.String()
        notes = graphene.String()

    def mutate(self, info, name, patient_id, name_, age, gender, doctor, medication, stage, notes):
        user = info.context.user or None

        p_profile = PatientProfile(patient_id=patient_id, name=name_, age=age, gender=gender, doctor=doctor,
                                   medication=medication, stage=stage, notes=notes)
        p_profile.save()

        return CreatePatientProfile(
            patient_id=patient_id, name=name_, age=age, gender=gender, doctor=doctor, medication=medication,
            stage=stage, notes=notes)



class Query(graphene.ObjectType):
	#results = graphene.List(StmType, id = graphene.Int())
    caregiver_profile = graphene.List(CaregiverProfileType, un = graphene.String())
    doctor_profile = graphene.List(DoctorProfileType, un = graphene.String())
    patient_profile = graphene.List(PatientProfileType, un = graphene.String())
	
    def resolve_caregiver_profile(self, info, un=None, **kwargs):
        if un:
            filter = (
                Q(username=un)
            )
            return CaregiverProfile.objects.filter(filter)

        return CaregiverProfile.objects.all()

    def resolve_doctor_profile(self, info, username=None, **kwargs):
        return DoctorProfile.objects.all()

    def resolve_patient_profile(self, info, username=None, **kwargs):
        return PatientProfile.objects.all()

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
    create_patient_profile = CreatePatientProfile.Field()
