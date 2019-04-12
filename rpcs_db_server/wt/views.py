from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from wt.models import Patient, Caregiver, Safezone
import json


# Create your views here.

@csrf_exempt
def patient(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'patient_id', 'wt_patient_id')
    if request.method == "GET":
        return return_data(request, Patient, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Patient, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def caregiver(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'caregiver_id', 'wt_caregiver_id')
    if request.method == "GET":
        return return_data(request, Caregiver, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Caregiver, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def safezone(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'radius', 'patient_id', 'wt_safezone_id')
    if request.method == "GET":
        return return_data(request, Safezone, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Safezone, my_fields)
    else:
        return handle_invalid_request(request)





