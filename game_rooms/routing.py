from django.urls import re_path
from .consumers import RoomConsumer

websocket_urlpatterns = [
    re_path('ws/room/', RoomConsumer.as_asgi()),
]








