from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from hs.models import Events
import json


# Create your views here.

@csrf_exempt
def events(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Events.objects.all()
        print(data.last().sensor_id)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Events(event_type = payload['event_type'], sensor_id = payload['sensor_id'], 
        sensor_type = payload['sensor_type'], timestamp = payload['timestamp'], 
        data = payload['data'], event_id = payload['event_id'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404



    








