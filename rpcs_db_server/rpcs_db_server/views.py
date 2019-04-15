from django.http import HttpResponse, Http404, JsonResponse
from rpcs_db_server.utils import authorized


def health(request):
    return HttpResponse('Server is up and running!')


def auth(request): 
    if request.method != "GET":        
        return HttpResponse('Invalid HTTP Method', status=405)

    if not authorized(request, None):
        return HttpResponse('Unauthorized', status=401)
        
    return HttpResponse("Permissions are encapsulated by username")

