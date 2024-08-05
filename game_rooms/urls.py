from django.urls import path
from .views import RoomApi

urlpatterns = [
    path('', RoomApi.as_view()),
    path('<id_code>/', RoomApi.as_view()),
]
