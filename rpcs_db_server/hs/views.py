from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hs.models import Events, Sensors
from rpcs_db_server.utils import authorized, ingest_data, return_data, handle_invalid_request, \
    json_timestamp_customizer, json_j2str_customizer
from hs.ca import update_br_usage
import psycopg2
import threading
import datetime as dt
from pytz import timezone
import json

# Download the helper library from https://www.twilio.com/docs/python/install
import twilio
from twilio.rest import Client

account_sid = 'ACcb394859c733f5274639779eab2cb0a4'
auth_token = '6470e99bc9d9373f286f89e647db5ec7'
client = Client(account_sid, auth_token)
est = timezone('US/Eastern')
cd_length = dt.timedelta(minutes=5)

br_gateway_id = 'c76c5d12-6647-11e9-a923-1681be663d3e'
br_motion_id = 'c26e4e88-2ecb-42ff-8482-4af80307a485'


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
        response = ingest_data(request, Events, my_fields, json_customizer=hs_customizer)
        if response.status_code == 200:
            threading.Thread(target=hs_alert).start()
        return response
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


@csrf_exempt
def hs_alert():
    try:
        connection = psycopg2.connect(user='rpcs', password='rpcs2019', host='localhost', port='', database='rpcs')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print('Error while fetching data from postgresql', error)
    else:
        query = "select * from hs_events order by timestamp desc limit 1"
        cursor.execute(query)
        new_data = cursor.fetchone()
        # stove analysis
        if "STOVE_HOT" in new_data[4] or "STOVE_WARM" in new_data[4]:
            message = client.messages \
                .create(
                body='Stove Hot Alert at ' + str(dt.datetime.now(tz=est)),
                from_='+14125672824',
                to='+14126166415'
            )
        # main door analysis
        elif "Main door opened" in new_data[4]:
            message = client.messages \
                .create(
                body='Main Door Opened at ' + str(dt.datetime.now(tz=est)),
                from_='+14125672824',
                to='+14126166415'
            )
        # bathroom usage analysis
        elif "rfid" in new_data[2] or "pir" in new_data[2]:
            if update_br_usage(new_data):
                message = client.messages \
                    .create(
                    body='Bathroom entry alert at ' + str(dt.datetime.now(tz=est)),
                    from_='+14125672824',
                    to='+14126166415'
                )
        elif "test_xiaoyu" in new_data[2]:
            message = client.messages \
                .create(
                body='Postman test at ' + str(dt.datetime.now(tz=est)),
                from_='+14125672824',
                to='+14126166415'
            )
    finally:
        if connection:
            cursor.close()
            connection.close()
