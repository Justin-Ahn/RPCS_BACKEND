from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import base64

def is_authorized(request, action):
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

