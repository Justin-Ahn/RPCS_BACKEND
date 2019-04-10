from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from wt.models import Patient, Caregiver, Safezone
import json


# Create your views here.

@csrf_exempt
def patient(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Patient.objects.all()
        print(data.last().patient_id)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]

        print("payload:")
        print(payload)

        newObject = Patient(location=payload['location'], timestamp=payload['timestamp'], patient_id=['patient_id'],
        wt_patient_id=payload['wt_patient_id'])

        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

@csrf_exempt
def caregiver(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Caregiver.objects.all()
        print(data.last().event_id)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]

        print("payload:")
        print(payload)

        newObject = Caregiver(location=payload['location'], timestamp=payload['timestamp'],
        caregiver_id=payload['caregiver_id'], wt_caregiver_id=payload['wt_caregiver_id'])

        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

@csrf_exempt
def safezone(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Safezone.objects.all()
        print(data)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]

        print("payload:")
        print(payload)

        newObject = Safezone(location=payload['location'], radius=payload['radius'], patient_id=payload['patient_id'], wt_safezone_id = ['wt_safezone_id'])

        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404




