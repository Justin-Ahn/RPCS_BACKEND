from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request
from stm.models import Results


# Create your views here.
@csrf_exempt
def tests(request):
    if not authorized(request, "stm"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('patient_name', 'patient_id', 'scaled_rating1', 'scaled_rating2', 'test_results')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Results, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Results, my_fields)
    else:
        return handle_invalid_request(request)



    








