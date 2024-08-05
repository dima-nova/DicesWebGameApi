from rest_framework import serializers, validators
from .models import RoomModel
from werkzeug.security import generate_password_hash
from authorization.models import User


class RoomSerializer(serializers.Serializer):
    """
    Serializer for the RoomModel. This serializer handles the conversion
    of RoomModel instances to and from JSON, and includes validation for
    the input data.

    Fields:
    - name: CharField, maximum length 100. Represents the name of the room.
    - max_players: IntegerField, default 2. Specifies the maximum number of players allowed in the room.
    - is_private: BooleanField, default False. Indicates if the room is private or public.
    - password: CharField, maximum length 218, allows blank. Used for the room's password if it is private.
    - author: SlugRelatedField, uses the 'slug' field from the user model specified in settings.AUTH_USER_MODEL.

    Methods:
    - validate_max_players: Validates that 'max_players' is between 2 and 6. Raises a ValidationError if outside this range.
    - create: Creates a new RoomModel instance from the validated data.
    """

    name = serializers.CharField(max_length=100)
    max_players = serializers.IntegerField()
    id_code = serializers.CharField(read_only=True)
    is_started = serializers.BooleanField(read_only=True)
    is_private = serializers.BooleanField(default=False)
    password = serializers.CharField(max_length=218, required=False, write_only=True)
    players_list = serializers.StringRelatedField(many=True, required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def validate_max_players(self, max_players):
        if not (2 <= max_players <= 6):
            raise validators.ValidationError(f"Max_players value must be from 2 to 6. But you set {max_players}")
        return max_players

    def validate(self, data):
        try:
            if data["is_private"]:
                if data["password"] == "":
                    raise validators.ValidationError("If the room is private, it must have password")
                data["password"] = generate_password_hash(data["password"])
            else:
                data["password"] = ""
        except KeyError:
            raise validators.ValidationError("If the room is private, it must have password")
        
        return data

    def create(self, validated_data):
        # print(validated_data)
        return RoomModel.objects.create(**validated_data)
