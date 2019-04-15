from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import modelform_factory
from datetime import datetime
import json
import base64

def authorized(request, action):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return False

    token_type, _, creds = auth_header.partition(' ')
    username, password = base64.b64decode(creds).decode().split(":")
   
    user = authenticate(username=username, password=password)
    
    if user is not None:       
        return True
        #name = user.get_username()
        #Need to actually add permissions & check permissions
    else:
        return False


def json_timestamp_customizer(json_data):
    if 'timestamp' in json_data:  # A disgusting hack but this will do...
        if json_data['timestamp'] is None:
            json_data['timestamp'] = datetime.now()
        else:
            json_data['timestamp'] = datetime.strptime(json_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

def json_j2str_customizer(json_data):
    if 'data' in json_data:
        json_data['data'] = json.dumps(json_data['data'])

def ingest_data(request, model, fields, json_customizer=None):
    payload = json.loads(request.body.decode())
    received_data = []
    form = modelform_factory(model, fields=fields)

    def valid_json_fields(fields, json_data):
        for field in fields:
            if field not in json_data:
                return False
        return True

    for json_entry in payload:
        if json_customizer is not None:
            json_customizer(json_entry)

        populated_form = form(data=json_entry)

        if valid_json_fields(fields, json_entry) and populated_form.is_valid():
            received_data.append(populated_form)
        else:
            return HttpResponse('RPCS Backend Server: Data push denied -- invalid params.', status=400)

    for data_entry in received_data:
        data_entry.save()

    response_text = 'RPCS Backend Server: Accepted ' + \
                    str(len(received_data)) + (' entry' if len(received_data) == 1 else ' entries')
    return HttpResponse(response_text, status=200)


def return_data(request, model, param):
    target = request.GET.get(param, '')
    try:
        pid_to_get = int(target)
    except ValueError:
        if target == '':
            pid_to_get = None
        else:
            return HttpResponse('RPCS Backend Server: Data pull denied -- invalid params.', status=400)

    all_data = serializers.serialize('json', model.objects.all())
    data_list = json.loads(all_data)
    mapped_list = list(map(lambda x: x['fields'], data_list))  # 'fields' -> a relic of how django processes data

    if pid_to_get is not None:
        response = list(filter(lambda x: x[param] == pid_to_get, mapped_list))
    else:
        response = mapped_list

    return HttpResponse(json.dumps(response), content_type='application/json', status=200)


def handle_invalid_request(request):
    response_text = 'RPCS Backend Server: Invalid HTTP request method'
    return HttpResponse(response_text, status=405)
