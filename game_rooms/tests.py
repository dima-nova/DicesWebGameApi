from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from werkzeug.security import check_password_hash
from .models import RoomModel
import jwt
from django.conf import settings
from django.test.utils import override_settings


class RoomViewTest(TestCase):
    url = "/api/room/"

    def get_jwt_token(self):
        data = {
            "username": "username",
            "password": "password123"
        }

        response = self.client.post("/api/auth/signup/", data=data, format="json")
        if "token" in response.data:
            payload = jwt.decode(response.data["token"], settings.SECRET_KEY, algorithms=['HS256'])
            return {'token': response.data["token"], 'user_id': payload["user_id"]}
        raise Exception("Bad request. User did not create")
    
    def get_room_id_code(self, jwt_token, room_name, max_players, is_private, password):
        data = {
            "name": room_name,
            "max_players": max_players,
            "is_private": is_private,
            "password": password
        }
        headers = {
            "Authorization": jwt_token
        }

        response = self.client.post("/api/room/", data=data, headers=headers, format="json")

        if 'id_code' in response.data["data"]:
            return response.data["data"]["id_code"]
        raise Exception("Bad request. Room did not create")

    def setUp(self):
        self.client = APIClient()

        user_data = self.get_jwt_token()
        self.token = user_data["token"]
        self.user_id = user_data["user_id"]
        self.room_name = "room_name"
        self.password = "123"
        self.max_players = 3
        self.is_private = True

        self.room_id_code = self.get_room_id_code(self.token, self.room_name, self.max_players, self.is_private, self.password)


    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_successful_post_request(self):
        data = {
            "name": self.room_name,
            "max_players": self.max_players,
            "is_private": self.is_private,
            "password": self.password
        }
        headers = {
            "Authorization": self.token
        }

        response = self.client.post(self.url, data=data, headers=headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], f"Room {self.room_name} created successfully.")
        self.assertIn('data', response.data)

        self.assertIn('id_code', response.data["data"])

        room = RoomModel.objects.get(id_code=response.data["data"]["id_code"])

        self.assertEqual(self.room_name, room.name)
        self.assertEqual(self.max_players, room.max_players)
        self.assertEqual(self.is_private, room.is_private)
        self.assertTrue(check_password_hash(room.password, self.password))

    
    def test_not_given_jwt_post_request(self):
        data = {
            "name": self.room_name,
            "max_players": self.max_players,
            "is_private": self.is_private,
            "password": self.password
        }

        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["errors"], 'Invalid token.')

    def test_missing_data_post_request(self):
        data = {
            "name": self.room_name,
            "max_players": self.max_players,
            "is_private": self.is_private,
            # Password is missing
        }
        headers = {
            "Authorization": self.token
        }

        response = self.client.post(self.url, data=data, headers=headers, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"], "{'non_field_errors': [ErrorDetail(string='If the room is private, it must have password', code='invalid')]}")
        
    def test_successful_get_request(self):
        url = f"{self.url}{self.room_id_code}/"

        headers = {
            "Authorization": self.token
        }

        response = self.client.get(url, headers=headers)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], self.room_name)
        self.assertEqual(data['max_players'], self.max_players)
        self.assertEqual(data['id_code'], self.room_id_code)
        self.assertIn('is_started', data)
        self.assertEqual(data['is_private'], self.is_private)
        self.assertEqual(data['author'], self.user_id)

    def test_not_given_jwt_get_request(self):
        url = f"{self.url}{self.room_id_code}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)