from django.shortcuts import render
from int.models import CaregiverProfile, DoctorProfile
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer

# Create your views here.

@csrf_exempt
def caregiver_profile(request):
    if not authorized(request, "int"):
        return HttpResponse('Unauthorized', status=41)

    my_fields = ('name', 'username', 'password', 'patient_id', 'schedule')
    if request.method == "GET":
        return return_data(request, CaregiverProfile, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, CaregiverProfile, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def doctor_profile(request):
    if not authorized(request, "int"):
        return HttpResponse('Unauthorized', status=41)

    my_fields = ('name', 'username', 'password', 'patient_id', 'appointment')
    if request.method == "GET":
        return return_data(request, DoctorProfile, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, DoctorProfile, my_fields)
    else:
        return handle_invalid_request(request)


