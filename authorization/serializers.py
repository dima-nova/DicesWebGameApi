from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.Serializer):
    """
    Serializer for user data with validation and creation of User instances.

    Fields:
    - username: Required; maximum length of 150 characters; unique validation.
    - password: Required; maximum length of 500 characters; must be at least 5 characters long.
    - rank_points: Optional; integer field.
    - image_number: Optional; integer field.

    Methods:
    - validate_password(value): Validates that the password is at least 5 characters long.
    - create(validated_data): Creates a new User instance with the validated data.
    - update(instance, validated_data): Updates the password of an existing User instance and saves the changes.
    """

    username = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=500, write_only=True)
    rank_points = serializers.IntegerField(required=False)
    image_number = serializers.IntegerField(required=False)


    def validate_password(self, value):
        if len(value) < 5:
           raise serializers.ValidationError("Password is too short; please ensure it meets the"
                                             " minimum length requirement of at least 5 characters.")
        return value


    def create(self, validated_data):
            user = User.objects.create(
                username=validated_data["username"],
                password=validated_data["password"],
            )

            return user
    

    def update(self, instance, validated_data):
        new_password = validated_data["password"]
        instance.password = new_password

        instance.save()

        print(instance)

        return instance