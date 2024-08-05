from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings
from authorization.models import User

def jwt_required(funct):
    def wrapper(self, request, *args, **kwargs):

        token = request.headers.get("Authorization", None)
        if token is not None or token != "":
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response({'errors': 'Token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'errors': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.get(pk=payload["user_id"])
            request.data["user"] = user
        else:
            return Response({'errors': 'Token is missing.'}, status=status.HTTP_401_UNAUTHORIZED)
        return funct(self, request, *args, **kwargs)

    return wrapper


