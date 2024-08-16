from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/users/'  # Adjust to your registration endpoint URL
        self.login_url = '/auth/jwt/create/'  # Adjust to your JWT login endpoint URL
        self.user_data = {
            "email": "newuser@example.com",
            "phone_number": "11111178393",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password": "password123"
        }

        # Register a user
        self.response = self.client.post(self.register_url, self.user_data, format='json')

        # Login to obtain JWT token
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        # Handle missing 'access' key gracefully
        self.token = login_response.data.get('refresh', None)
        if self.token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_register_user(self):
        data = {
            "email": "anotheruser@example.com",
            "phone_number": "22290278390",
            "first_name": "Another",
            "username": "anotheruser",
            "last_name": "User",
            "password": "password123"
        }
        response = self.client.post(self.register_url, data, format='json')
        print("Register User Response:", response.data)  # Debug output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)  # Check if ID is in the response

    def test_login_user(self):
        data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = self.client.post('/auth/jwt/create/', data)  # Adjust to your current user endpoint URL
        print("Get Current User Response:", response.data)  # Debug output
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)  # Check if ID is in the response
        # Check other fields as needed
