from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ca.models import Wandering, Phys_measure, Phys_incidents, Phys_params
import json


# Create your views here.

@csrf_exempt
def wandering(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'caregiver_id', 'is_wandering', 'alerted')
    if request.method == "GET":
        return return_data(request, Wandering, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Wandering, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def phys_measures(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'age', 'gender', 'stage', 'weight', 'body_fat', 'skinny_fat', 'bp_low', 'bp_high',
                 'pr_low', 'pr_high', 'rr_low', 'rr_high')
    if request.method == "GET":
        return return_data(request, Phys_measure, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Phys_measure, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def phys_incidents(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'incident_id', 'timestamp', 'pulse_rate', 'respiratory_rate', 'blood_pressure',
                 'incident_type', 'recording')
    if request.method == "GET":
        return return_data(request, Phys_incidents, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Phys_incidents, my_fields)
    else:
        return handle_invalid_request(request)

    
@csrf_exempt
def phys_params(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'coef_bp', 'coef_pr', 'coef_rr', 'bias_logit', 'ar')
    if request.method == "GET":
        return return_data(request, Phys_params, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Phys_params, my_fields)
    else:
        return handle_invalid_request(request)