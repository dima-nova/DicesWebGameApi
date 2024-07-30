from django.db import models
from django.contrib.auth.models import AbstractUser
from .settings import *


class User(AbstractUser):
    """
    A user model that extends the standard AbstractUser model.

    Fields:
    - password (CharField): Stores the user's password as a string. Maximum length is 512 characters.
    - rank_points (IntegerField): The user's rank points. Default value is 1000.
    - image_number (IntegerField): The user`s profile picture number. It can be from 1 to 5

    Methods:
    - __str__(): Returns the username of the user.
    - save(): set default values.
    """

    password = models.CharField(max_length=512)
    rank_points = models.IntegerField(default=1000)
    image_number = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        self.rank_points = BASIC_RANK_POINTS
        self.image_number = BASIC_IMAGE_NUMBER

        super().save(*args, **kwargs)