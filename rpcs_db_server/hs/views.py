from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hs.models import Events, Sensors
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, \
    json_timestamp_customizer, json_j2str_customizer
import psycopg2
import requests

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
        response = ingest_data(request, Sensors, my_fields)
        #if response.status_code == 200:
            #stove_analysis()
        requests.post("http://www.redoxygen.net/sms.dll?Action=SendSMS&AccountId=CI00206082&Email=annanm%40andrew%2Ecmu%2Eedu&Password=XddAv8r8&Recipient=4126166415&Message=Stove+Hot+Alert!!!")    
        return response
    else:
        return handle_invalid_request(request)
    
@csrf_exempt
def stove_analysis():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgresql', error)
    else:
        query = "select * from hs_events order by timestamp desc limit 1"
        cursor.execute(query)
        new_stove_data = cursor.fetchone()
        if "STOVE_HOT" in new_stove_data[4]:
            requests.post("http://www.redoxygen.net/sms.dll?Action=SendSMS&AccountId=CI00206082&Email=annanm%40andrew%2Ecmu%2Eedu&Password=XddAv8r8&Recipient=4129236982&Message=StoveHot Alert!!!")
    finally:
        if connection:
            cursor.close()
            connection.close()







