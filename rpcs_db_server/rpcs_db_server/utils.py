from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import modelform_factory
from datetime import datetime, timedelta
import json
import base64

response_prefix = "RPCS Backend Server: "


def authorized(request, action):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return False

    token_type, _, creds = auth_header.partition(' ')
    username, password = base64.b64decode(creds).decode().split(":")
   
    user = authenticate(username=username, password=password)

    # A really bad hack for permissions but hopefully this will suffice. Permissions currently depend on parsing
    # username & seeing that it corresponds with the api endpoint the user is hitting
    if user is not None:
        return action is None or \
               user.is_superuser or \
               request.method == "GET" and "readonly" in username or \
               action in username
    return False


# This is our spec for datetime!
def str_2_dt(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')


def str_2_date(s):
    return datetime.strptime(s, '%Y-%m-%d')


def json_timestamp_customizer(json_data):
    if 'timestamp' in json_data:  # A disgusting hack but this will do...
        if json_data['timestamp'] is None:
            json_data['timestamp'] = datetime.now()
        else:
            try:
                json_data['timestamp'] = str_2_dt(json_data['timestamp'])
                # Add 1 microsecond (change won't be view-able) to keep trailing zeros in dt string
                json_data['timestamp'] += timedelta(microseconds=1) 
            except ValueError:
                return False
        return True
    return False


def json_j2str_customizer(json_data):
    if 'data' in json_data:
        try:
            json_data['data'] = json.dumps(json_data['data'])
        except TypeError:
            return False
    return True


def ingest_data(request, model, fields, json_customizer=None):
    try:
        payload = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(response_prefix + "Not a valid Json!", status=400)
    if not isinstance(payload, list):
        return HttpResponse(response_prefix + "Requires payloads to be a JSON array", status=400)

    received_data = []
    form = modelform_factory(model, fields=fields)

    def valid_json_fields(fields, json_data):
        for field in fields:
            if field not in json_data:
                return False
        return True

    for json_entry in payload:
        custom_success = True
        if json_customizer is not None:
            custom_success = json_customizer(json_entry)

        populated_form = form(data=json_entry)

        if valid_json_fields(fields, json_entry) and populated_form.is_valid() and custom_success:
            received_data.append(populated_form)
        else:
            error_msg = response_prefix + 'Data push denied -- invalid payload. \n\n' + \
                        'Both conditions need to be met -- \n' + \
                        'All Json fields are present: ' + str(valid_json_fields(fields, json_entry)) + '\n' + \
                        'The Json data should be valid. Errors: ' + str(populated_form.errors.as_data())

            return HttpResponse(error_msg, status=400)

    for data_entry in received_data:
        data_entry.save()

    response_text = response_prefix + 'Accepted ' + str(len(received_data)) + (' entry' if len(received_data) == 1 else
                                                                               ' entries')
    return HttpResponse(response_text, status=200)


# KV store of the query param & a tuple of (Converting user given val to required obj for comparison, filtering action)
filter_actions = {
        "patient_id": (lambda given_param: int(given_param),
                       lambda data, patient_id: list(filter(lambda x: x["patient_id"] == patient_id, data))),

        "caregiver_id": (lambda given_param: int(given_param),
                         lambda data, caregiver_id: list(filter(lambda x: x["caregiver_id"] == caregiver_id, data))),

        "doctor_id": (lambda given_param: int(given_param),
                      lambda data, doctor_id: list(filter(lambda x: x["doctor_id"] == doctor_id, data))),

        "event_id": (lambda given_param: int(given_param),
                     lambda data, event_id: list(filter(lambda x: x["event_id"] == event_id, data))),

        "incident_id": (lambda given_param: int(given_param),
                        lambda data, incident_id: list(filter(lambda x: x["incident_id"] == incident_id, data))),

        "sensor_id": (lambda given_param: given_param,  # No-op for this one
                      lambda data, sensor_id: list(filter(lambda x: x["sensor_id"] == sensor_id, data))),
    
        "event_type": (lambda given_param: given_param,  # No-op for this one
                      lambda data, event_type: list(filter(lambda x: x["event_type"] == event_type, data))),

        "time_start": (lambda given_param: str_2_dt(given_param),
                       lambda data, time_start: list(filter(lambda x: str_2_dt(x["timestamp"]) >= time_start, data))),

        "time_end": (lambda given_param: str_2_dt(given_param),
                     lambda data, time_end: list(filter(lambda x: str_2_dt(x["timestamp"]) <= time_end, data))),

        "date_start": (lambda given_param: str_2_date(given_param),
                       lambda data, date_start: list(filter(lambda x: str_2_date(x["date"]) >= date_start, data))),

        "date_end": (lambda given_param: str_2_date(given_param),
                     lambda data, date_end: list(filter(lambda x: str_2_date(x["date"]) <= date_end, data)))
    }
CONVERSION_ACTION = 0  # 0th element in tuple above is the conversion action
FILTERING_ACTION = 1  # 1st element in tuple above is the filtering action


def return_data(request, model, query_filter_params):
    all_objects = serializers.serialize('json', model.objects.all())
    json_objects = json.loads(all_objects)
    response_data = list(map(lambda x: x['fields'], json_objects))  # 'fields' -> a relic of how django processes data

    for param in query_filter_params:
        user_params = request.GET.get(param, '')
        if user_params == '':
            continue
        try:
            param_value = filter_actions[param][CONVERSION_ACTION](user_params)
        except ValueError:
            return HttpResponse(response_prefix + 'Data pull denied -- invalid query params.', status=400)

        try:
            response_data = filter_actions[param][FILTERING_ACTION](response_data, param_value)
        except ValueError:
            return HttpResponse(response_prefix + 'Something failed on our end... Please contact Justin', status=400)

    return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


def handle_invalid_request(request):
    response_text = response_prefix + 'Invalid HTTP request method'
    return HttpResponse(response_text, status=405)
