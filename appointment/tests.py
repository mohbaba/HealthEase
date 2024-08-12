from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from users.models import UserProfile
from .models import Patient, Doctor, Appointment


class AppointmentTests(APITestCase):
    def setUp(self):
        self.patient_user = UserProfile.objects.create_user(
            username='patientuser',
            email='patient@example.com',
            password='password123',
            phone_number='0987654321',
            first_name='Jane',
            last_name='Doe'
        )
        self.doctor_user = UserProfile.objects.create_user(
            username='doctoruser',
            email='doctor@example.com',
            password='password123',
            phone_number='0987654323',
            first_name='John',
            last_name='Doe'
        )
        self.patient = Patient.objects.create(user_profile=self.patient_user)

        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\signature.jpg", 'rb') as f:
            self.signature = f.read()

        self.doctor = Doctor.objects.create(
            user_profile_id=self.doctor_user.id,
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
        self.appointment_data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment_date': '2024-08-10T10:00:00Z',
            'reason': 'Routine check-up'
        }

        self.appointment = Appointment.objects.create(
            patient_id=self.patient.id,
            doctor_id=self.doctor.id,
            appointment_date='2024-08-10T10:00:00Z',
            reason='Complaints'
        )
        self.client.force_authenticate(user=self.patient_user)  # authenticate the client as the patient user

    def test_create_appointment(self):
        url = reverse('appointment-list')
        response = self.client.post(url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(Appointment.objects.get(id=response.data.get('id')).reason, response.data.get('reason'))

    def test_retrieve_appointment(self):
        # appointment = Appointment.objects.create(**self.appointment_data)
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reason'], 'Complaints')

    def test_retrieve_appointment_by_non_owner(self):
        url = reverse('appointment-detail', args=[self.appointment.id])
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to view this appointment.')

    def test_update_appointment(self):
        # appointment = Appointment.objects.create(**self.appointment_data)
        url = reverse('appointment-detail', args=[self.appointment.id])
        updated_data = {'reason': 'Follow-up'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Appointment.objects.get(id=self.appointment.id).reason, 'Follow-up')

    def test_delete_appointment(self):
        # appointment = Appointment.objects.create(**self.appointment_data)
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
