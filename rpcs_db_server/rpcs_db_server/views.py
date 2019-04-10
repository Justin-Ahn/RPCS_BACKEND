from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse


def health(request):
    if request.method != "GET":     
        raise Http404("HTTP Verbs Accepted: GET")	
    return HttpResponse('Server is up and running!')


def auth(request): 
    if request.method != "GET":        
        raise Http404("HTTP Verbs Accepted: GET")	
    # Need to check Auth header, decode, and describe permissions. 
    return JsonResponse({'foo':'auth'})

