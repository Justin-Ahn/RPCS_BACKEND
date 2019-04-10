from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def tests(request):
    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)

    if request.method == "GET":
        return HttpResponse('GET', status=200)
    elif request.method == "POST":
        return HttpResponse('Accepted', status=200)
    else:
        raise HTTP404



    








