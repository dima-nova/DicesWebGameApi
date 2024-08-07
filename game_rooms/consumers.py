from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import RoomModel
from .serializers import RoomSerializer
from django.conf import settings


class RoomConsumer(WebsocketConsumer):
    """
    WebSocket consumer for managing real-time updates for game rooms.

    Methods:
    - connect(self): Handles WebSocket connection requests.
        - Adds the channel to the 'rooms' group and accepts the connection.
        - Retrieves all rooms that have not yet started and sends this data to all members of the 'rooms' group.

    - disconnect(self, code): Handles WebSocket disconnection requests.
        - Removes the channel from the 'rooms' group.
        - Logs a message when a user disconnects.

    - chat_message(self, event): Handles messages from the 'rooms' group.
        - Receives a message event and sends the message data back to the WebSocket client.

    - get_all_rooms(self): Retrieves all rooms that have not yet started from the database.
        - Serializes the data using `RoomSerializer` and returns it.
    """


    room_group_name = settings.GAME_ROOMS_CHANNEL_GROUP_NAME

    def connect(self):

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        rooms = self.get_all_rooms()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": rooms}
            )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print("User disconnected")

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message,
        }))

    def get_all_rooms(self):
        rooms = RoomModel.objects.filter(is_started=False)
        serializer = RoomSerializer(instance=rooms, many=True)
        return serializer.data