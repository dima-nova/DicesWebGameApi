from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import UserSerializer
from werkzeug.security import generate_password_hash
import jwt
from django.conf import settings
from .login_service import authenticate_user


class SignUpView(APIView):
    """
    API view for user registration.

    Methods:
    - get(request): Handles GET requests and returns a 405 Method Not Allowed error.
    - post(request): Handles POST requests for user registration. Validates input data using UserSerializer,
      hashes the password, creates a new User instance, and returns a success message along with a JWT token
      for the newly created user. If validation fails, returns a 400 Bad Request with validation errors.
    """

    def get(self, request):
        return Response(data={"errors": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            hashed_password = generate_password_hash(request.data["password"])

            user = serializer.save()
            user.password = hashed_password
            user.save()

            payload = {
                "user_id": user.pk,
                "username": user.username
            }
            token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')

            return Response(data={"message": f"{user.username} was created.", "token": token}, status=status.HTTP_201_CREATED)

        return Response(data={"errors": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.

    Methods:
    - get(request): Handles GET requests and returns a 405 Method Not Allowed error.
    - post(request): Handles POST requests for user login. Authenticates the user using `authenticate_user` function.
    - If authentication is successful, returns a 200 OK response with a success message and a JWT token.
    - If authentication fails, returns a 401 Unauthorized response with an error message.
    - If required data is missing, returns a 400 Bad Request response with an error message.

    Raises:
    - KeyError: If the 'username' or 'password' key is missing from the request data.
    """

    def get(self, request):
        return Response(data={"errors": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user_data = authenticate_user(username, password)

            if user_data["authenticated"]:

                user = user_data["user"]
                payload = {
                    "user_id": user.pk,
                    "username": user.username
                }
                token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
                return Response(data={"message": user_data["message"], "token": token}, status=status.HTTP_200_OK)

            else:
                return Response(data={"message": user_data["message"]}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response(data={"errors": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
