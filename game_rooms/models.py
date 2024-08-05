from django.utils import timezone
from django.db import models
from . import fields
from django.conf import settings
import time
from authorization.models import User


class RoomModel(models.Model):
    """
    RoomModel represents a room in the application.

    Attributes:
    - name (str): The name of the room.
    - id_code (str): A unique identifier for the room like "A1B2C3". Must not be set manually.
    - max_players (int): The maximum number of players allowed in the room. Default is 2.
    - is_private (bool): Indicates if the room is private. Default is False.
    - password (str): The password for the room if it is private. Must be None or empty if is_private is False.
    - players_list (ManyToManyField): A list of players in the room. Must include the author.
    - author (ForeignKey): The user who created the room.
    - is_started (bool): Indicates if the room has started. Must not be set manually.
    - created_at (DateTimeField): The timestamp when the room was created. Must not be set manually.
    - delete_at (DateTimeField): The timestamp when the room will be deleted. Must not be set manually.

    Methods:
    - save(self, *args, **kwargs): Saves the room instance. Sets created_at and delete_at if the instance is new.
                                     Adds the author to the players_list.
    - add_user_to_list(self, user_pk): Adds a user to the players_list by their primary key.
    - delete_user_from_list(self, user_pk): Removes a user from the players_list by their primary key.
    - start_create_timer(self): Starts a timer for 10 seconds and then sets is_started to True.
    """

    name = models.CharField(max_length=100)
    id_code = fields.IdCodeField(blank=True)  # --------------------------------------- | Must not be set
    max_players = models.IntegerField(default=2)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=218,
                                blank=True)  # ---------------- | If is_private == False: set None or empty
    players_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="rooms",
        blank=True
    )  # ---------------------------------------------- | DONE must have author in list
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="own_rooms"
    )
    is_started = models.BooleanField(default=False)  # -------------------------------- | Must not be set
    created_at = models.DateTimeField(blank=True,
                                      auto_now_add=True)  # --------------------------- | Must not be set
    delete_at = models.DateTimeField(blank=True)  # ----------------------------------- | Must not be set

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
            self.delete_at = self.created_at + timezone.timedelta(seconds=settings.SECONDS_BEFORE_START_GAME_ROOM) 

        super().save(*args, **kwargs)

        self.players_list.add(self.author.pk)

            
    def add_user_to_list(self, user_pk):
        user = User.objects.get(pk=user_pk)

        self.players_list.add(user)
        self.save(update_fields=["players_list"])

    def delete_user_from_list(self, user_pk):
        user = settings.AUTH_USER_MODEL.objects.get(pk=user_pk)

        self.players_list.remove(user)
        self.save(update_fields=["players_list"])

    def start_create_timer(self):
        time.sleep(settings.SECONDS_BEFORE_START_GAME_ROOM)

        self.is_started = True
        self.save(update_fields=["is_started"])
