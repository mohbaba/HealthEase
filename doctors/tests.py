from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctors.models import Doctor, Medicine, Prescription, DoctorsNote
from patients.models import Patient, MedicalRecords
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

        doctors_note = DoctorsNote.objects.create(
            doctor=Doctor.objects.get(id=self.doctor.data['id']),
            patient=self.patient,
            condition_description='Patient shows symptoms of a mild cold.',
            recommendations='Rest and stay hydrated.',
            doctor_signature='path/to/signature.png'
        )

        self.patient.doctors_notes.add(doctors_note)

    def register_doctor(self):
        response = self.client.post(self.register_doctor_url, self.doctor_data, format='multipart')
        return response

    def test_register_doctor(self):
        self.user_profile = {
            'username': 'doctor2',
            'password': 'password123',
            "phone_number": "0912345678",
            'email': 'doctor2@mailerg.com',
            'first_name': 'Moh',
            'last_name': 'Baba'
        }

        self.register_user_url = reverse('register-user')
        register_user_response = self.client.post(self.register_user_url, self.user_profile)

        self.register_doctor_url = reverse('register_doctor')
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\JAVA\DiaryUML.jpg", 'rb') as f:
            image_data = f.read()
        self.register_doctor_data = {
            'user_profile': register_user_response.data['id'],
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

        response = self.client.post(self.register_doctor_url, self.register_doctor_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_profile'], register_user_response.data['id'])
        self.assertEqual(response.data['license_number'], self.register_doctor_data['license_number'])

    def test_create_medicine(self):
        self.drug = {
            'drug_name': 'Tylenol',
            'medication_form': 'Tablet',
            'dosage': 2,
            'no_times': 3,
            'frequency': 'Daily',
            'meal_instruction': 'After meal',
            'start_date': '2024-08-03',
            'drug_unit_of_weight': 'mg'
        }
        self.drug_url = reverse('add-drug')
        response = self.client.post(self.drug_url, self.drug)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 3)
        self.assertEqual(Medicine.objects.get(id=response.data['id']).drug_name, 'Tylenol')

    def create_drugs(self):
        drugs = ['Paracetamol', 'Tylenol', 'Lonart']
        new_drugs = []
        for drug in drugs:
            medicine = Medicine.objects.create(
                drug_name=drug,
                dosage=2,
                medication_form='Tablet',
                drug_unit_of_weight='mg',
                no_times=3,
                frequency='Daily',
                meal_instruction='After meal',
                start_date='2024-08-05',
            )
            new_drugs.append(medicine)
        return new_drugs

    def test_prescribe_drugs_for_patient(self):
        self.prescription_url = reverse('prescribe')
        drugs = self.create_drugs()
        print(drugs)
        prescription = {
            'doctor': self.doctor.data['id'],
            'patient': self.patient.id,
            'prescribed_drugs': [
                {
                    'drug_name': 'Paracetamol',
                    'dosage': 2,
                    'medication_form': 'Tablet',
                    'drug_unit_of_weight': 'mg',
                    'no_times': 3,
                    'frequency': 'Daily',
                    'meal_instruction': 'After meal',
                    'start_date': '2024-08-05',
                },
                {
                    'drug_name': 'Tylenol',
                    'dosage': 2,
                    'medication_form': 'Tablet',
                    'drug_unit_of_weight': 'mg',
                    'no_times': 3,
                    'frequency': 'Daily',
                    'meal_instruction': 'After meal',
                    'start_date': '2024-08-05',
                }
            ]
        }
        print(UserProfile.objects.all().count())
        response = self.client.post(self.prescription_url, prescription, format='json')
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['patient_firstname'], 'Jane')
        self.assertEquals(response.data['patient_lastname'], 'Doe')
        self.assertEqual(Prescription.objects.count(), 1)
        self.assertEqual(Prescription.objects.get().prescribed_drugs.count(), 2)
