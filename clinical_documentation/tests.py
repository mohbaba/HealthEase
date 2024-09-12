from django.test import TestCase
from rest_framework.test import APITestCase

from clinical_documentation.models import ClinicalNote
from users.models import UserProfile


# Create your tests here.
class DocumentationTestCase(APITestCase):
    def setUp(self):
        self.patient_user = UserProfile.objects.create_user(
            username='patientuser',
            email='patient@example.com',
            password='password123',
            phone_number='0987654321',
            first_name='Jane',
            last_name='Doe'
        )