from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from ga.models import Logical, Semantic, Procedural, Episodic
import json


# Create your views here.

@csrf_exempt
def logical(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'logical_score', 'timestamp', 'game_id')
    if request.method == "GET":
        return return_data(request, Logical, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Logical, my_fields)
    else:
        return handle_invalid_request(request)

    
@csrf_exempt
def semantic(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'semantic_score', 'timestamp')
    if request.method == "GET":
        return return_data(request, Semantic, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Semantic, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def procedural(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'procedural_score', 'timestamp')
    if request.method == "GET":
        return return_data(request, Procedural, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Procedural, my_fields)
    else:
        return handle_invalid_request(request)
    

@csrf_exempt
def episodic(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'episodic_score', 'timestamp', 'question', 'answer_choices',
                 'patient_answer', 'correct_answer')
    if request.method == "GET":
        return return_data(request, Episodic, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Episodic, my_fields)
    else:
        return handle_invalid_request(request)



    








