from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from doctors.models import Doctor


class UserTest(APITestCase):

    def register_doctor(self):
        data = {
            "email": "Aj@gmail.com",
            "phone_number": "2229098453",
            "first_name": "Ajiri",
            "username": "Aj@gmail.com",
            "last_name": "Nemesis",
            "password": "password123",
            "role": "DOCTOR",
            "gender": "Male"
        }
        response = self.client.post('/auth/users/', data, format='json')
        return response

    def create_doctor_with_user(self, user_profile_id):
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\signature.jpg", 'rb') as f:
            self.signature = f.read()
        doctor = Doctor.objects.create(
            user_profile_id=user_profile_id,
            license_number=1234567890,
            signature=SimpleUploadedFile("signature.jpg", self.signature, content_type="image/jpg"),
            registration_number=123456,
            registration_council='Medical Council',
            registration_year='2020-01-01',
            rating=5,
            specialty='CARDIOLOGY',
            consultation_fee=500,
            qualification='MBBS',
            college='Medical College',
            start_year='2010-01-01',
            end_year='2015-01-01',
            is_available=True
        )
        return doctor

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
            "password": "password123",
            "gender": "Female"
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

    def test_custom_user_login_view(self):
        doctor = self.register_doctor()
        self.create_doctor_with_user(doctor.data.get('id'))
        doctor_login_data = {
            "email": doctor.data.get('email'),
            "password": "password123"
        }
        url = reverse('login')
        response = self.client.post(url, doctor_login_data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('refresh_token', response.data)  # Check if token is in the response
        self.assertEqual(response.data['user']['email'], doctor.data.get('email'))
        self.assertEqual(response.data['user']['role'], doctor.data.get('role'))
