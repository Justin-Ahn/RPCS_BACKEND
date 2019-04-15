from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from watch.models import Patient, Event


# Create your views here.

@csrf_exempt
def patient(request):
    if not authorized(request, "watch"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_name', 'patient_id', 'event', 'event_id')
    if request.method == "GET":
        return return_data(request, Patient, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Patient, my_fields)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def events(request):
    if not authorized(request, "watch"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('event_id', 'event_description', 'event_category')
    if request.method == "GET":
        return return_data(request, Event, 'event_id')
    elif request.method == "POST":
        return ingest_data(request, Event, my_fields)
    else:
        return handle_invalid_request(request)
    
