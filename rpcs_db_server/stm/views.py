from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from stm.models import Results
import json


# Create your views here.

@csrf_exempt
def tests(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        data = Results.objects.all()
        print(data.last().patient_id)

        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Results(patient_name = payload['patient_name'], patient_id = payload['patient_id'], 
        scaled_rating1 = payload['scaled_rating1'], scaled_rating2 = payload['scaled_rating2'], 
        test_results = payload['test_results'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404



    








