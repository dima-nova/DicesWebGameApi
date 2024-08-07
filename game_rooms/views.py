from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import RoomSerializer
from .models import RoomModel
from .decorators import jwt_required
from .tasks import start_room_timer


class RoomApi(APIView):
    """
    API view for managing game rooms.

    Methods:
    - get(request, id_code=None): Handles GET requests to retrieve room details.
        - If the room with the given `id_code` exists, returns a 200 OK response with the room data.
        - If the room does not exist, returns a 404 Not Found response with an error message.
        - Requires JWT authentication.

    - post(request): Handles POST requests to create a new room.
        - Expects `name` and `user` fields in the request data.
        - If required fields are missing, returns a 400 Bad Request response with an error message.
        - If the request data is valid, creates a new room, starts a room timer asynchronously, and returns a 201 Created response with a success message and the room data.
        - If the data is invalid, returns a 400 Bad Request response with validation errors.
        - Requires JWT authentication.

    Raises:
    - KeyError: If the `name` or `user` key is missing from the request data.
    """

    @jwt_required
    def get(self, request, id_code=None):
        try:
            room = RoomModel.objects.get(id_code=id_code)
            serializer = RoomSerializer(instance=room)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except RoomModel.DoesNotExist:
            return Response(data={f"Room with id_code '{id_code}' does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @jwt_required
    def post(self, request):
        try:
            data = request.data

            name = data["name"]
            author = data["user"]
        except KeyError:
            return Response(data={"errors": "Not found correct fields."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RoomSerializer(data={
            **request.data,
            "author": author.pk,
            })
        if serializer.is_valid():
            serializer.save()
            room_id_code = serializer.data["id_code"]
            start_room_timer.delay(room_id_code=room_id_code)

            return Response(data={"message": f"Room {name} created successfully.", "data": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(data={"errors": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
