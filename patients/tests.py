from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import UserProfile


# Create your tests here.

class TestPatients(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_profile()
        self.register_user_url = reverse('register-user')
        self.register_user_response = self.client.post(self.register_user_url, self.user_profile_data)
        self.user_profile = UserProfile.objects.create(**self.user_profile_data)
        self.user_profile.save()
        self.register_patient_url = reverse('register_patient')
        self.create_medical_records()
        self.create_patient_data()

    def test_register_patient(self):
        response = self.client.post(self.register_patient_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_profile'], self.register_user_response.data)
        self.assertEqual(response.data['address'], self.patient_data['address'])
        self.assertEqual(response.data['date_of_birth'], self.patient_data['date_of_birth'])

    def create_patient_data(self):
        self.patient_data = {
            'user_profile': self.user_profile.id,
            'medical_records': self.medical_records.id,
            'date_of_birth': '2000, 1, 1',
            'gender': 'Female',
            'blood-group': 'A+',
            'emergency_contact_name': 'shola',
            'emergency_contact_contact': '+2348106317491'
        }

    def create_medical_records(self):
        self.medical_records = {
            'allergies': 'Lactose',
            'current_medication': 'abidec',
            'past_medication': 'ACCULOL',
            'chronic_disease': 'Asthma',
            'incident': 'Burns',
            'surgeries': 'Lungs',
            'smoking_habit': 'I dont smoke',
            'alcohol_habit': 'Non-drinker',
            'lifestyle': 'Moderately active',
            'food_preference': 'Vegetarian'
        }

    def create_user_profile(self):
        self.user_profile_data = {
            'username': 'patient1',
            'password': 'password456',
            'email': 'patient1@gmail.com',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
