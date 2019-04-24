from ct.models import Trend
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer


# Create your views here
@csrf_exempt
def patient_trends(request):
    if not authorized(request, "ct"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_id', 'test_score', 'num_falls', 'num_injuries', 'weight', 'body_fat_percentage')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Trend, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Trend, my_fields)
    else:
        return handle_invalid_request(request)



    








