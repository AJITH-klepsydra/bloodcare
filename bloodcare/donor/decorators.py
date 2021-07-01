from rest_framework.response import Response

from bloodcare.interface.models import Recipient


def is_authenticated(func):
    def inner(obj, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return func(obj, request, *args, **kwargs)
        
        token = request.headers.get('Authorization', None)
        
        if not token:
            return Response({"message": "UnAuthenticated"}, status=401)
        try:
            request.user = Recipient.objects.get(key=token)
        except Exception:
            return Response({"message": "UnAuthenticated"}, status=401)
        return func(obj, request, *args, **kwargs)

    return inner
