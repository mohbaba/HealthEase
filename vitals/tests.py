from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctors.models import DoctorsNote, Doctor
from patients.models import Patient, MedicalRecords
from users.models import UserProfile


# Create your tests here.

class VitalsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profile = UserProfile.objects.create(
            username='patientuser',
            email='patient@example.com',
            password='password123',
            phone_number='0987654321',
            first_name='Jane',
            last_name='Doe'
        )

        self.medical_records = MedicalRecords.objects.create(
            allergies='Lactose',
            current_medications='Abidec',
            past_medications='Accord Bendroflumethiazide',
            chronic_disease='Diabetes',
            incident='Burns',
            surgeries='Heart',
            smoking_habit='NOT_SMOKER',
            alcohol_habit='NON_DRINKER',
            lifestyle='LOW',
            food_preferences='VEGETARIAN'
        )

        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\signature.jpg", 'rb') as f:
            self.signature = f.read()

        self.doctor = Doctor.objects.create(
            user_profile=self.user_profile,
            license_number=123456,
            signature=SimpleUploadedFile('signature.jpg', self.signature, 'image/jpg'),
            registration_number=123456,
            registration_council='Medical Council',
            registration_year='2020-01-01',
            rating=5,
            specialty='CARDIOLOGY',
            consultation_fee=100,
            qualification='MD',
            college='Medical College',
            start_year='2015-01-01',
            end_year='2020-01-01',
            is_available=True
        )

        self.patient = Patient.objects.create(
            user_profile=self.user_profile,
            medical_records=self.medical_records
        )

        self.doctors_note = DoctorsNote.objects.create(
            doctor=Doctor.objects.get(id=self.doctor.id),
            patient=self.patient,
            purpose='Patient shows symptoms of a mild cold.',
            recommendations='Rest and stay hydrated.',
            doctor_signature=SimpleUploadedFile('signatureImage', self.signature, 'image/jpg')
        )

        self.patient.doctors_notes.add(self.doctors_note)

    def test_add_blood_pressure_to_patient(self):
        url = reverse('add_blood_pressure')
        data = {
            'systolic': 120,
            'diastolic': 80,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('systolic'), data.get('systolic'))
        self.assertEqual(response.data.get('diastolic'), data.get('diastolic'))
