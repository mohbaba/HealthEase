from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


# Create your tests here.

class TestPatients(APITestCase):
    def setUp(self):
        self.client = APIClient()

