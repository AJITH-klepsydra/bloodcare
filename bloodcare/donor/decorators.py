from bloodcare.interface.models import Recipient
from rest_framework.response import Response
from rest_framework import status

def is_authenticated(func):
    def inner(obj,request,*args,**kwargs):
        token = request.headers.get('Authorization',None)
        if not token:
            return Response({"info":"UnAuthenticated"},status= 401)
        try:
            request.user = Recipient.objects.get(key = token)
        except:
            return Response({"info":"UnAuthenticated"},status= 401)

        return func(obj,request,*args,**kwargs)
    return inner
