from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctors.models import Doctor
from users.models import UserProfile


# Create your tests here.

class TestDoctors(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_profile_data = {
            'username': 'doctor1',
            'password': 'password123',
            'email': 'doctor1@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        self.user_profile = UserProfile()
        self.user_profile.save()
        self.register_doctor_url = reverse('register_doctor')

        self.doctor_data = {
            'user_profile': self.user_profile.id,
            'license_number': 1234567890,
            'signature': SimpleUploadedFile("signature.png", b"file_content", content_type="image/png"),
            'registration_number': 123456,
            'registration_council': 'Medical Council',
            'registration_year': '2020-01-01',
            'rating': 5,
            'specialty': 'Cardiology',
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
        self.assertEqual(response.data['user_profile'], self.user_profile.id)
        self.assertEqual(response.data['license_number'], self.doctor_data['license_number'])
