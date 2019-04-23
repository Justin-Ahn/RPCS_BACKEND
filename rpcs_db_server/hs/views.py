from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hs.models import Events, Sensors
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, \
    json_timestamp_customizer, json_j2str_customizer


# Create your views here.

@csrf_exempt
def events(request):
    if not authorized(request, "hs"):
        return HttpResponse('Unauthorized', status=401)

    def hs_customizer(json_entry):  # Not 100% "functional"... but eh?
        success1 = json_timestamp_customizer(json_entry)
        success2 = json_j2str_customizer(json_entry)
        return success1 and success2

    my_fields = ('event_type', 'sensor_id', 'sensor_type', 'data', 'timestamp')
    filterable_params = ['sensor_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Events, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Events, my_fields, json_customizer=hs_customizer)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def sensors(request):
    if not authorized(request, "hs"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'sensor_type', 'sensor_id', 'patient_id')
    filterable_params = ['sensor_id', 'patient_id']
    if request.method == "GET":
        return return_data(request, Sensors, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Sensors, my_fields)
    else:
        return handle_invalid_request(request)
    








