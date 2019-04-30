from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, json_timestamp_customizer
from wt.models import Patient, Caregiver, Safezone
from wt.ca import update_wandering
import psycopg2
import threading
import datetime
from pytz import timezone

# Download the helper library from https://www.twilio.com/docs/python/install
import twilio
from twilio.rest import Client

account_sid = 'ACcb394859c733f5274639779eab2cb0a4'
auth_token = '6470e99bc9d9373f286f89e647db5ec7'
client = Client(account_sid, auth_token)
est = timezone('US/Eastern')


@csrf_exempt
def patient(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'patient_id')
    filterable_params = ['patient_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Patient, filterable_params)
    elif request.method == "POST":
        response = ingest_data(request, Patient, my_fields, json_customizer=json_timestamp_customizer)
        if response.status_code == 200:
            threading.Thread(target=wandering_analysis).start()
        return response
    else:
        return handle_invalid_request(request)


@csrf_exempt
def caregiver(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'timestamp', 'caregiver_id')
    filterable_params = ['caregiver_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Caregiver, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Caregiver, my_fields, json_customizer=json_timestamp_customizer)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def safezone(request):
    if not authorized(request, "wt"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('location', 'radius', 'patient_id')
    filterable_params = ['patient_id']
    if request.method == "GET":
        return return_data(request, Safezone, filterable_params)
    elif request.method == "POST":
        return ingest_data(request, Safezone, my_fields)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def wandering_analysis():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgresql', error)
    else:
        query = "select * from wt_patient order by timestamp desc limit 1"
        cursor.execute(query)
        new_wandering_data = cursor.fetchone()
        if update_wandering(new_wandering_data):
            message = client.messages \
                .create(
                body='Stove Hot Alert at ' + str(datetime.datetime.now(tz=est)),
                from_='+14125672824',
                to='+14126166415'
            )
    finally:
        if connection:
            cursor.close()
            connection.close()
