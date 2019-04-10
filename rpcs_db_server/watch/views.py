from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from watch.models import Patient, Event
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

        newObject = Patient(patient_name=payload['patient_name'], patient_id=payload['patient_id'],
        event=payload['event'], event_id=payload['event_id'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

@csrf_exempt
def events(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Event.objects.all()
        print(data.last().event_id)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]

        print("payload:")
        print(payload)

        newObject = Event(event_id=payload['event_id'], event_description=payload['event_description'],
                          event_category=payload['event_category'])

        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404
    











# Create your views here.
