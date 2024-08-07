from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import RoomModel
from .serializers import RoomSerializer
from django.conf import settings


@receiver(post_save, sender=RoomModel)
def send_new_room_created(sender, instance, **kwargs):  
    room = RoomModel.objects.get(id_code=instance.id_code)

    if instance.is_started:
        message = {"message": f"Room {instance.name} started.",
               "type": "delete",
               "data": RoomSerializer(instance=room).data
            }
    else:
        message = {"message": f"New room {instance.name} created!",
               "type": "create",
               "data": RoomSerializer(instance=room).data
            }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.GAME_ROOMS_CHANNEL_GROUP_NAME, {"type": "chat.message", "message": message}
    )
