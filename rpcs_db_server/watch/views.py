from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, \
    json_timestamp_customizer
from watch.models import Patient, Event
import psycopg2
import threading
import datetime

# Download the helper library from https://www.twilio.com/docs/python/install
import twilio
from twilio.rest import Client

account_sid = 'ACcb394859c733f5274639779eab2cb0a4'
auth_token = '6470e99bc9d9373f286f89e647db5ec7'
client = Client(account_sid, auth_token)


# Create your views here.

@csrf_exempt
def patient(request):
    if not authorized(request, "watch"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('event_id', 'event_description', 'event_category', 'timestamp')
    filterable_params = ['event_id', 'time_start', 'time_end']
    if request.method == "GET":
        return return_data(request, Event, filterable_params, json_customizer=json_timestamp_customizer)
    elif request.method == "POST":
        return ingest_data(request, Patient, my_fields)
    else:
        return handle_invalid_request(request)


@csrf_exempt
def events(request):
    if not authorized(request, "watch"):
        return HttpResponse('Unauthorized', status=401)

    my_fields = ('event_id', 'event_description', 'event_category')
    filterable_params = ['event_id']
    if request.method == "GET":
        return return_data(request, Event, filterable_params)
    elif request.method == "POST":
        res = ingest_data(request, Event, my_fields)
        if res.status_code == 200:
            threading.Thread(target=fall_alert).start()
        return res
    else:
        return handle_invalid_request(request)


@csrf_exempt
def fall_alert():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgresql', error)
    else:
        query = "select * from watch_event order by id desc limit 1"
        cursor.execute(query)
        new_data = cursor.fetchone()
        if "fall" in new_data[3]:
            message = client.messages \
                .create(
                body='Falling Alert at ' + str(datetime.datetime.now()),
                from_='+14125672824',
                to='+14126166415'
            )
            print(message.error_message)
    finally:
        if connection:
            cursor.close()
            connection.close()
