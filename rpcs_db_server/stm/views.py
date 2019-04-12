from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from stm.models import Results
from django.forms.models import modelform_factory
import json

# Create your views here.
@csrf_exempt
def tests(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_name', 'patient_id', 'scaled_rating1', 'scaled_rating2', 'test_results')
    if request.method == "GET":
        return return_data(request, Results, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Results, my_fields)
    else:
        return handle_invalid_request(request)



    








