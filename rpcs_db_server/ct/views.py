from ct.models import Profile, Incident, Trend
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer


# Create your views here.

@csrf_exempt
def patient_profile(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'name', 'age', 'gender', 'doctor', 'medication', 'stage', 'notes')
    if request.method == "GET":
        return return_data(request, Profile, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Profile, my_fields)
    else:
        return handle_invalid_request(request)

    
@csrf_exempt
def patient_incidents(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'incident_id', 'timestamp', 'pulse_rate', 'respiratory_rate', 'blood_pressure',
                 'incident_type', 'recording')
    if request.method == "GET":
        return return_data(request, Incident, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Incident, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def patient_trends(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'test_score', 'num_falls', 'num_injuries', 'weight', 'body_fat_percentage')
    if request.method == "GET":
        return return_data(request, Trend, 'patient_id')
    elif request.method == "POST":
        return ingest_data(request, Trend, my_fields)
    else:
        return handle_invalid_request(request)



    








