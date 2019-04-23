from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ga.models import Logical, Semantic, Procedural, Episodic
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer


# Create your views here.

@csrf_exempt
def logical(request):
    if not authorized(request, "ga"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'logical_score', 'timestamp', 'game_id')
    filterable_params = ['patient_id', 'time_start']
    if request.method == "GET":
        return return_data(request, Logical, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Logical, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)

    
@csrf_exempt
def semantic(request):
    if not authorized(request, "ga"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'semantic_score', 'timestamp')
    filterable_params = ['patient_id', 'time_start']
    if request.method == "GET":
        return return_data(request, Semantic, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Semantic, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def procedural(request):
    if not authorized(request, "ga"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'procedural_score', 'timestamp')
    filterable_params = ['patient_id', 'time_start']
    if request.method == "GET":
        return return_data(request, Procedural, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Procedural, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)
    

@csrf_exempt
def episodic(request):
    if not authorized(request, "ga"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'episodic_score', 'timestamp', 'question', 'answer_choices',
                 'patient_answer', 'correct_answer')
    filterable_params = ['patient_id', 'time_start']
    if request.method == "GET":
        return return_data(request, Episodic, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Episodic, my_fields,  json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)



    








