from django.apps import AppConfig


class GameRoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game_rooms'

    def ready(self) -> None:
        import game_rooms.signals