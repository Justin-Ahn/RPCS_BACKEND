from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer
from wt.models import Patient, Caregiver, Safezone


@csrf_exempt
def patient(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'patient_id')
    filterable_params = ['patient_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Patient, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Patient, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def caregiver(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'caregiver_id')
    filterable_params = ['caregiver_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Caregiver, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Caregiver, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def safezone(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'radius', 'patient_id')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Safezone, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Safezone, my_fields)
    else:
        return handle_invalid_request(request)
