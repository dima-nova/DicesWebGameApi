from werkzeug.security import check_password_hash
from .models import User

def authenticate_user(username, password):
    """
    Authenticate a user by username and password.

    Args:
    - username (str): The username of the user.
    - password (str): The password to authenticate.

    Returns:
    - dict: {"authenticated": True, "user": user, "message": "User logged in successfully."} if the password is correct.
    - dict: {"authenticated": False, "message": "Password is incorrect."} if the password is incorrect.
    - dict: {"authenticated": False, "message": "User by this username does not exist."} if the user does not exist.
    """

    try:
        user = User.objects.get(username=username)

        try:
            if check_password_hash(user.password, password):
                return {"authenticated": True, "user": user, "message": "Login successful."}
            else:
                return {"authenticated": False, "message": "Password is incorrect."}
        except AttributeError:
            return {"authenticated": False, "message": "Incorrect data type"}

    except User.DoesNotExist:
        return {"authenticated": False, "message": "User by this username does not exist."}
