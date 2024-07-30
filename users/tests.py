from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# Create your tests here.

class UserTest(APITestCase):

    def test_register_user(self):
        self.client = APIClient()
        self.url = reverse('register-user')
        self.user_data = {
            "email": "newuser@example.com",
            "phone_number": "1234567890",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password": "password123"
        }
        response = self.client.post(self.url, self.user_data)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
