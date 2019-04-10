from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import is_authorized
import base64


def health(request):
    if request.method != "GET":     
        raise Http404("HTTP Verbs Accepted: GET")	
    return HttpResponse('Server is up and running!')


def auth(request): 
    if request.method != "GET":        
        raise Http404("HTTP Verbs Accepted: GET")	

    if not is_authorized(request):
        return HttpResponse('Unauthorized', status=401)
        
    return JsonResponse({'foo':'auth'})

