from ca.models import Wandering, Phys_measure, Phys_incidents, Phys_params, Sleep_trend, Incident_summary
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer


# Create your views here.

@csrf_exempt
def wandering(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'caregiver_id', 'is_wandering', 'alerted')
    filterable_params = ['patient_id', 'caregiver_id']
    if request.method == "GET":
        return return_data(request, Wandering, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Wandering, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def phys_measures(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'age', 'gender', 'stage', 'weight', 'body_fat', 'skinny_fat', 'bp_low', 'bp_high',
                 'pr_low', 'pr_high', 'rr_low', 'rr_high')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Phys_measure, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Phys_measure, my_fields)
    else:
        return handle_invalid_request(request)

@csrf_exempt
def phys_incidents(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'incident_id', 'timestamp', 'pulse_rate', 'respiratory_rate', 'blood_pressure',
                 'incident_type', 'recording')
    filterable_params = ['patient_id', 'incident_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Phys_incidents, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Phys_incidents, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)

    
@csrf_exempt
def phys_params(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'coef_bp', 'coef_pr', 'coef_rr', 'bias_logit', 'ar')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Phys_params, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Phys_params, my_fields)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def sleep_trends(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'date', 'hours_slept', 'hours_in_bed', 'num_wake_up', 'num_get_out_of_bed',
                 'num_go_to_bathroom')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Sleep_trend, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Sleep_trend, my_fields)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def incident_summary(request):
    if not authorized(request, "ca"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'date', 'num_ltm_lapse', 'num_stm_lapse', 'num_falls', 'num_wandering')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Incident_summary, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Incident_summary, my_fields)
    else:
        return handle_invalid_request(request)
