from config.celery import app
import time
from .models import RoomModel


@app.task
def start_room_timer(room_id_code):
    try:
        room = RoomModel.objects.get(id_code=room_id_code)
        room.start_create_timer()
        
    except RoomModel.DoesNotExist:
        return False
    
    return room.is_started
