from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctors.models import DoctorsNote, Doctor
from patients.models import Patient, MedicalRecords
from users.models import UserProfile
from vitals.models import BloodPressure, BloodSugar, HeartRate, BMI, Temperature, Height, Weight, Vitals


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
            medical_records=self.medical_records,

        )

        self.doctors_note = DoctorsNote.objects.create(
            doctor=Doctor.objects.get(id=self.doctor.id),
            patient=self.patient,
            purpose='Patient shows symptoms of a mild cold.',
            recommendations='Rest and stay hydrated.',
            doctor_signature=SimpleUploadedFile('signatureImage', self.signature, 'image/jpg')
        )

        self.patient.doctors_notes.add(self.doctors_note)

        self.blood_pressure = BloodPressure.objects.create(systolic=120, diastolic=80)
        self.blood_sugar = BloodSugar.objects.create(measurement=100, measuring_state='Fasting')
        self.heart_rate = HeartRate.objects.create(bpm=70)
        self.bmi = BMI.objects.create(bmi=22)
        self.temperature = Temperature.objects.create(temperature=37, unit='Celcius')
        self.weight = Weight.objects.create(weight=70, unit='Kilograms')
        self.height = Height.objects.create(weight=170, unit='Centimeters')

        self.vitals_data = {
            'patient': self.patient.id,
            'weight': self.weight.id,
            'height': self.height.id,
            'temperature': self.temperature.id,
            'bmi': self.bmi.id,
            'heart_rate': self.heart_rate.id,
            'blood_pressure': self.blood_pressure.id,
            'blood_sugar': self.blood_sugar.id,
        }

        self.vitals = Vitals.objects.create(
            patient=self.patient, weight=self.weight, height=self.height, temperature=self.temperature,
            bmi=self.bmi, heart_rate=self.heart_rate, blood_pressure=self.blood_pressure, blood_sugar=self.blood_sugar
        )


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

    def test_get_blood_pressure_from_patient(self):
        blood_pressure = BloodPressure.objects.create(
            systolic=120,
            diastolic=80
        )
        url = reverse('blood_pressure', kwargs={'pk': blood_pressure.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('systolic'), blood_pressure.systolic)
        self.assertEqual(response.data.get('diastolic'), blood_pressure.diastolic)

    def test_create_vitals(self):

        url = reverse('vitals-list')
        response = self.client.post(url, self.vitals_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vitals.objects.count(), 2)

    def get_vitals_data(self):
        return {
            'patient': self.patient,
            'weight': self.weight,
            'height': self.height,
            'temperature': self.temperature,
            'bmi': self.bmi,
            'heart_rate': self.heart_rate,
            'blood_pressure': self.blood_pressure,
            'blood_sugar': self.blood_sugar,
        }

    def test_retrieve_vitals(self):
        vitals_data = self.get_vitals_data()
        vitals = Vitals.objects.create(**vitals_data)
        url = reverse('vitals-detail', args=[vitals.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient'], self.patient.id)

    def test_update_vitals(self):
        data = {
            'patient': self.patient.id,
            'weight': self.weight.id,
            'height': self.height.id,
            'temperature': self.temperature.id,
            'bmi': self.bmi.id,
            'heart_rate': self.heart_rate.id,
            'blood_pressure': self.blood_pressure.id,
            'blood_sugar': self.blood_sugar.id,
        }
        url = reverse('vitals-detail', kwargs={'pk': self.vitals.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vitals(self):
        # Create initial vitals record
        vitals_data = self.get_vitals_data()
        vitals = Vitals.objects.create(**vitals_data)

        # Prepare the partial update data
        new_weight = Weight.objects.create(weight=75, unit='Kilograms')
        updated_data = {
            'weight': {
                'weight': new_weight.weight,
                'unit': new_weight.unit,
                'last_recorded': new_weight.last_recorded
            }
        }

        # Perform the partial update
        url = reverse('vitals-detail', kwargs={'pk': vitals.pk})
        response = self.client.patch(url, updated_data, format='json')

        # Print the response for debugging
        print(response.data)

        # Validate the response and database update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vitals.objects.get(id=vitals.id).weight.weight, 75)

    def test_delete_vitals(self):

        url = reverse('vitals-detail', kwargs={'pk': self.vitals.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vitals.objects.count(), 0)
