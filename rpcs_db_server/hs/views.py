from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hs.models import Events
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, \
    json_timestamp_customizer, json_j2str_customizer


# Create your views here.

@csrf_exempt
def events(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    def hs_customizer(json_entry):  # Not 100% "functional"... but eh?
        json_timestamp_customizer(json_entry)
        json_j2str_customizer(json_entry)

    my_fields = ('event_type', 'sensor_id', 'sensor_type', 'data', 'timestamp', 'event_id')
    if request.method == "GET":
        return return_data(request, Events, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Events, my_fields, json_customizer=hs_customizer)
    else:
        return handle_invalid_request(request)

    








