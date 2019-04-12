from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from hs.models import Events
import json


# Create your views here.

@csrf_exempt
def events(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('event_type', 'sensor_id', 'sensor_type', 'data', 'timestamp', 'event_id')
    if request.method == "GET":
        return return_data(request, Events, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Events, my_fields)
    else:
        return handle_invalid_request(request)

    








