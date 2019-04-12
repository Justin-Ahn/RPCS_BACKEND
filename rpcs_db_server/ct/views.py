from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ct.models import Profile, Incident, Trend
import json


# Create your views here.

@csrf_exempt
def patient_profile(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        target = request.GET.get('patient_id', '')
        
        all_data = serializers.serialize('json', Profile.objects.all())
        data_list = json.loads(all_data)
        
        mapped_list = list(map(lambda x: x['fields'], data_list))
        response = list(filter(lambda x: x['patient_id'] == int(target), mapped_list))

        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Profile(patient_id = payload['patient_id'], name = payload['name'], 
        age = payload['age'], gender = payload['gender'], doctor = payload['doctor'],
        medication = payload['medication'], stage = payload['stage'], notes = payload['notes'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

    
@csrf_exempt
def patient_incidents(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Incident.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Incident(patient_id = payload['patient_id'], incident_id = payload['incident_id'], 
        timestamp = payload['timestamp'], pulse_rate = payload['pulse_rate'], respiratory_rate = payload['respiratory_rate'],
        blood_pressure = payload['blood_pressure'], incident_type = payload['incident_type'], recording = payload['recording'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404
    

@csrf_exempt
def patient_trends(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Trend.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Trend(patient_id = payload['patient_id'], test_score = payload['test_score'], 
        num_injuries = payload['num_injuries'], num_falls = payload['num_falls'], weight = payload['weight'],
        body_fat_percentage = payload['body_fat_percentage'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404



    








