from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ga.models import Logical, Semantic, Procedural, Episodic
import json


# Create your views here.

@csrf_exempt
def logical(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Logical.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Logical(patient_id = payload['patient_id'], logical_thinking_score = payload['logical_thinking_score'], 
        timestamp = payload['timestamp'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404

    
@csrf_exempt
def semantic(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Semantic.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Semantic(patient_id = payload['patient_id'], semantic_score = payload['semantic_score'], 
        timestamp = payload['timestamp'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404
    


@csrf_exempt
def procedural(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Procedural.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Procedural(patient_id = payload['patient_id'], procedural_score = payload['procedural_score'], 
        timestamp = payload['timestamp'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404
    

@csrf_exempt
def episodic(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        response_body = serializers.serialize('json', Episodic.objects.all())
        return HttpResponse(response_body, content_type='application/json', status=200)

    elif request.method == "POST":
        payload = json.loads(request.body.decode())[0]
        print("payload:")
        print(payload)
        newObject = Episodic(patient_id = payload['patient_id'], episodic_score = payload['episodic_score'], 
        timestamp = payload['timestamp'], question = payload['question'], 
        answer_choices = payload['answer_choices'], patient_answer = payload['patient_answer'],
        correct_answer = payload['correct_answer'])
        newObject.save()
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404



    








