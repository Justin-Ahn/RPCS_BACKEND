from django.http import HttpResponse
from django.shortcuts import render
from int.models import CaregiverProfile, DoctorProfile, PatientProfile
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer

# Create your views here.

@csrf_exempt
def caregiver_profile(request):
    if not authorized(request, "int"):
        return HttpResponse('Unauthorized', status=401)

    # A really hack-y way to support updates w/o duplicate data. Should actually be supported via updates.
    # This also has lots of bad side effects like deleting things despite the query not being well-formed
    def caregiver_pk_hack(json_data):
        if 'caregiver_id' in json_data:
            CaregiverProfile.objects.filter(caregiver_id=json_data['caregiver_id']).delete()
        return True

    my_fields = ('name', 'username', 'password', 'patient_id', 'schedule', 'caregiver_id')
    if request.method == "GET":
        return return_data(request, CaregiverProfile, 'caregiver_id')
    elif request.method == "POST":
        return ingest_data(request, CaregiverProfile, my_fields, json_customizer=caregiver_pk_hack)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def doctor_profile(request):
    if not authorized(request, "int"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('name', 'username', 'password', 'patient_id', 'appointment', 'doctor_id')
    if request.method == "GET":
        return return_data(request, DoctorProfile, 'doctor_id')
    elif request.method == "POST":
        return ingest_data(request, DoctorProfile, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def patient_profile(request):
    if not authorized(request, "int"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'name', 'age', 'gender', 'doctor', 'medication', 'stage', 'notes')
    if request.method == "GET":
        return return_data(request, PatientProfile, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, PatientProfile, my_fields)
    else:
        return handle_invalid_request(request)

