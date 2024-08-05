from django.db.models import CharField
from rest_framework.validators import ValidationError
import string
import random

class IdCodeField(CharField):
    """
    Custom Django field that generates a unique ID code consisting of 6 characters.
    The format of the code is three uppercase letters interspersed with three digits.
    Example: 'A1B2C3'

    Methods:
    __init__ - Initializes the IdCodeField with a maximum length of 6 characters and ensures
                that the field's value is unique within the database.
    generate_code - Generates a unique ID code consisting of 6 characters:
                    Uppercase letter, digit, uppercase letter, digit, uppercase letter, digit.
    generate_unique_code - Generates a unique ID code that does not already exist in the database.
                            Keeps generating codes until a unique one is found.
    pre_save - Prepares the field's value before saving the model instance.
                Generates a unique ID code and assigns it to the field.
    validate - Validates the value of the field before saving the model instance.
                Ensures that the field is not empty.
    """

    description = "Id code that keep unique set of simbols ('W3D5A9')."

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)

    def generate_code(self):
        """Generate unique id code. Example ('A1B2C3') """
        letters = string.ascii_uppercase
        digits = string.digits
        return f"{random.choice(letters)}{random.choice(digits)}{random.choice(letters)}{random.choice(digits)}{random.choice(letters)}{random.choice(digits)}"

    def generate_unique_code(self):
        while True:
            new_code = self.generate_code()
            try:
                room = self.model.objects.get(**{self.attname: new_code})
            except self.model.DoesNotExist:
                return new_code


    def pre_save(self, model_instance, add):
        value = self.generate_unique_code()
        setattr(model_instance, self.attname, value)

        return super().pre_save(model_instance, add)

    def validate(self, value, model_instance):
        if not value:
            raise ValidationError(f"{self.name} cannot be empty")
        super().validate(value, model_instance)



