from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash


class SignUpViewTest(TestCase):
    url = "/api/auth/signup/"

    def setUp(self):
        self.client = APIClient()
        self.username = "username"
        self.password = "password123"

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"errors": "Method not allowed."})

    def test_successful_post_request(self):
        data = {
            "username": self.username,
            "password": self.password
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

        self.assertEqual(response.data['message'], f'{self.username} was created.')

        user = User.objects.get(username=self.username)
        self.assertTrue(check_password_hash(user.password, self.password))

    def test_unsuccessful_post_request(self):
        data = {
            "username": self.username,
            # Password is missed
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)


class LoginViewTest(TestCase):
    url = "/api/auth/login/"

    def setUp(self):
        self.client = APIClient()
        self.username = 'username'
        self.password = generate_password_hash('password123')

        self.client.post("/api/auth/signup/", {"username": self.username, "password": self.password})

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"errors": "Method not allowed."})

    def test_successful_post_request(self):
        data = {
            "username": self.username,
            "password": self.password
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['message'], 'Login successful.')

    def test_unsuccessful_login_invalid_password(self):
        data = {
            'username': self.username,
            'password': 'wrong_password'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Password is incorrect.')

    def test_unsuccessful_login_invalid_username(self):
        data = {
            'username': "not_created_username",
            'password': self.password
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'User by this username does not exist.')

    def test_unsuccessful_login_invalid_data_type(self):
        data = {
            'username': self.username,
            'password': True
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Incorrect data type')

    def test_unsuccessful_login_missing_fields(self):
        data = {
            'username': self.username
            # Missing password
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], 'Invalid data')



