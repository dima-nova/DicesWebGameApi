import logging
from channels.middleware import BaseMiddleware
from authorization.models import User
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings

logger = logging.getLogger(__name__)

class TokenAuthenticationMiddleware(BaseMiddleware):
    """
    Middleware for authenticating WebSocket connections using JWT tokens.

    Methods:
    - __call__(self, scope, receive, send): Handles WebSocket connection requests.
        - Extracts the 'authorization' header from the request.
        - Decodes the JWT token to retrieve the user ID.
        - Fetches the user from the database based on the user ID.
        - Sets the `scope["user"]` to the authenticated user or an `AnonymousUser` if authentication fails.
        - If authentication fails due to an expired, invalid token, or missing token, closes the WebSocket connection with a 4000 code and logs an error.
        - Calls the parent class's `__call__` method to continue processing the request if authentication is successful.

    - get_user_by_id(self, user_id): Asynchronously retrieves a user from the database based on the provided user ID.
        - Returns the user object if found, otherwise returns `None`.

    Raises:
    - No specific exceptions are raised directly by this middleware, but logging is used to capture authentication errors.
    """

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = headers.get(b'authorization', b'').decode()

        scope["user"] = AnonymousUser()

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = await self.get_user_by_id(payload["user_id"])

                if user is not None:
                    scope["user"] = user
                else:
                    logger.error("User not found")
                    await send({"type": "websocket.close", "code": 4000})
                    return
            except jwt.ExpiredSignatureError:
                logger.error("Token has expired")
                await send({"type": "websocket.close", "code": 4000})
                return
            except jwt.InvalidTokenError:
                logger.error("Invalid token")
                await send({"type": "websocket.close", "code": 4000})
                return
        else:
            logger.error("Token is missing")
            await send({"type": "websocket.close", "code": 4000})
            return

        await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
