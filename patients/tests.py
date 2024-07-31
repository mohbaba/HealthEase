from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from users.models import UserProfile


# Create your tests here.

class TestPatients(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_profile()
        self.user_profile = UserProfile.objects.create(**self.user_profile_data)
        self.user_profile.save()
        self.register_patient_url = reverse('register_patient')
        self.medical_records = {
            'allergies': 'Lactose',
            'current_medication': 'adidec',
            'past_medication': ''
        }

        self.patient_data = {
            'user_profile': self.user_profile.id,
            'medical_records': self.medical_records.id,

        }

    def create_user_profile(self):
        self.user_profile_data = {
            'username': 'patient1',
            'password': 'password456',
            'email': 'patient1@gmail.com',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
