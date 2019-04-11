from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ca.models import Wandering, Phys_measure, Phys_incidents, Phys_params
import json


# Create your views here.

@csrf_exempt
def wandering(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Wandering.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Wandering(patient_id = payload['patient_id'], caregiver_id = payload['caregiver_id'], 
        isWandering = payload['isWandering'], alerted = payload['alerted'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

@csrf_exempt
def phys_measures(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Phys_measure.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Phys_measure(patient_id = payload['patient_id'], age = payload['age'], 
        gender = payload['gender'], stage = payload['stage'], weight = payload['weight'],
        body_fat = payload['body_fat'], skinny_fat = payload['skinny_fat'], bp_low = payload['bp_low'],
        bp_high = payload['bp_high'], pr_low = payload['pr_low'], pr_high = payload['pr_high'],
        rr_low = payload['rr_low'], rr_high = payload['rr_high'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

@csrf_exempt
def phys_incidents(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Phys_incidents.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Phys_incidents(patient_id = payload['patient_id'], incident_id = payload['incident_id'], 
        timestamp = payload['timestamp'], pulse_rate = payload['pulse_rate'], respiratory_rate = payload['respiratory_rate'],
        blood_pressure = payload['blood_pressure'], incident_type = payload['incident_type'], 
        recording = payload['recording'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

    
@csrf_exempt
def phys_params(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Phys_params.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Phys_params(patient_id = payload['patient_id'], coef_bp = payload['coef_bp'], 
        coef_pr = payload['coef_pr'], coef_rr = payload['coef_rr'], bias_logit = payload['bias_logit'],
        ar = payload['ar'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404