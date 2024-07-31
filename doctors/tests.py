from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctors.models import Doctor
from users.models import UserProfile


# Create your tests here.

class TestDoctors(APITestCase):
    #TODO: validate phone number, validate email

    def setUp(self):
        self.client = APIClient()
        self.user_profile_data = {
            'username': 'doctor1',
            'password': 'password123',
            "phone_number": "1234567890",
            'email': 'doctor1@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        self.register_user_url = reverse('register-user')
        self.register_user_response = self.client.post(self.register_user_url, self.user_profile_data)

        self.register_doctor_url = reverse('register_doctor')
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\JAVA\DiaryUML.jpg", 'rb') as f:
            image_data = f.read()
        self.doctor_data = {
            'user_profile': self.register_user_response.data['id'],
            'license_number': 1234567890,
            'signature': SimpleUploadedFile("DiaryUML.jpg", image_data, content_type="image/jpg"),
            'registration_number': 123456,
            'registration_council': 'Medical Council',
            'registration_year': '2020-01-01',
            'rating': 5,
            'specialty': 'CARDIOLOGY',
            'consultation_fee': 500,
            'qualification': 'MBBS',
            'college': 'Medical College',
            'start_year': '2010-01-01',
            'end_year': '2015-01-01',
            'is_available': True
        }

    def test_register_doctor(self):
        response = self.client.post(self.register_doctor_url, self.doctor_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_profile'], self.register_user_response.data['id'])
        self.assertEqual(response.data['license_number'], self.doctor_data['license_number'])

    # def test_register_doctor_without_pre_registration(self):

