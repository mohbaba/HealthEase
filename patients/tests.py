from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from doctors.models import Medicine, DoctorsNote, Doctor
from patients.models import Patient, MedicalRecords
from users.models import UserProfile


# Create your tests here.

class TestPatients(APITestCase):
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
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\signature.jpg", 'rb') as f:
            self.signature = f.read()
        self.doctor_data = {
            'user_profile': self.register_user_response.data['id'],
            'license_number': 1234567890,
            'signature': SimpleUploadedFile("signature.jpg", self.signature, content_type="image/jpg"),
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

        self.doctor = self.client.post(self.register_doctor_url, self.doctor_data, format='multipart')

        self.patient_user = UserProfile.objects.create_user(
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

        self.medicine1 = Medicine.objects.create(
            medication_form='Tablet',
            dosage=500,
            no_times=2,
            frequency='Daily',
            meal_instruction='With meal',
            start_date=timezone.now().date(),
            drug_name='Paracetamol',
            drug_unit_of_weight='mg'
        )

        self.medicine2 = Medicine.objects.create(
            medication_form='Capsule',
            dosage=250,
            no_times=3,
            frequency='Weekly',
            meal_instruction='After meal',
            start_date=timezone.now().date(),
            drug_name='Amoxicillin',
            drug_unit_of_weight='mg'
        )

        # Create Patient
        self.patient = Patient.objects.create(
            user_profile=self.patient_user,
            medical_records=self.medical_records
        )

        self.doctors_note = DoctorsNote.objects.create(
            doctor=Doctor.objects.get(id=self.doctor.data['id']),
            patient=self.patient,
            purpose='Patient shows symptoms of a mild cold.',
            recommendations='Rest and stay hydrated.',
            doctor_signature=SimpleUploadedFile('signatureImage', self.signature, 'image/jpg')
        )

        self.patient.doctors_notes.add(self.doctors_note)
        self.client.force_authenticate(user=UserProfile.objects.get(id=self.register_user_response.data.get('id')))

    def test_register_patient(self):
        url = reverse('patient')
        data = {'user_profile': self.patient_user}
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user_profile'), self.patient_user.id)
