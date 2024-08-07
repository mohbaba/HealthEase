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

    def prescription(self):
        self.prescription_url = reverse('prescribe')
        prescription_data = {
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
        prescription = self.client.post(self.prescription_url, prescription_data, format='json')
        return prescription

    def test_prescribe_drugs_for_patient(self):
        self.assertEquals(self.prescription().status_code, status.HTTP_201_CREATED)
        print(self.prescription())
        self.assertEquals(self.prescription().data['patient_firstname'], 'Jane')
        self.assertEquals(self.prescription().data['patient_lastname'], 'Doe')
        self.assertEqual(Prescription.objects.get(id=self.prescription().data.get('id')).prescribed_drugs.count(), 2)

    def get_image_file(self, path):
        with open(path, 'rb') as data:
            return SimpleUploadedFile("update_image", data.read(), content_type='image/jpg')

    def test_update_doctor(self):
        self.update_doctor_url = reverse('update-doctor', kwargs={'pk': self.doctor.data['id']})
        update_data = {
            'license_number': 987654,
            # 'signature': self.get_image_file(r"C:\Users\ENVY\Pictures\Camera Roll\photo_2022-01-10_09-09-21 (2).jpg"),
            'registration_number': 123123,
            'registration_council': 'New Medical Council',
            'registration_year': '2021-01-01',
            'rating': 4,
            'specialty': 'DERMATOLOGY',
            'consultation_fee': 300,
            'qualification': 'MD',
            'college': 'New Medical College',
            'start_year': '2016-01-01',
            'end_year': '2021-01-01',
            'is_available': False
        }

        response = self.client.patch(self.update_doctor_url, update_data, format='multipart')
        print(response.data)
        self.saved_doctor = Doctor.objects.get(id=self.doctor.data['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.saved_doctor.refresh_from_db()
        self.assertEqual(self.saved_doctor.license_number, update_data['license_number'])
        # self.assertEqual(self.saved_doctor.signature, update_data['signature'])
        self.assertEqual(self.saved_doctor.registration_number, update_data['registration_number'])
        self.assertEqual(self.saved_doctor.registration_council, update_data['registration_council'])
        self.assertEqual(str(self.saved_doctor.registration_year), update_data['registration_year'])
        self.assertEqual(self.saved_doctor.rating, update_data['rating'])
        self.assertEqual(self.saved_doctor.specialty, update_data['specialty'])
        self.assertEqual(self.saved_doctor.consultation_fee, update_data['consultation_fee'])
        self.assertEqual(self.saved_doctor.qualification, update_data['qualification'])
        self.assertEqual(self.saved_doctor.college, update_data['college'])
        self.assertEqual(str(self.saved_doctor.start_year), update_data['start_year'])
        self.assertEqual(str(self.saved_doctor.end_year), update_data['end_year'])
        self.assertEqual(self.saved_doctor.is_available, update_data['is_available'])

    def test_delete_medicine(self):
        self.delete_drug_url = reverse('medicine', kwargs={'pk': self.medicine2.id})
        response = self.client.delete(self.delete_drug_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medicine.objects.count(), 1)

    def test_update_medicine(self):
        self.update_data = {
            'drug_name': 'Updated Aspirin',
            'dosage': 200,
            'medication_form': 'Capsule',
            'drug_unit_of_weight': 'mg',
            'no_times': 2,
            'frequency': 'Weekly',
            'meal_instruction': 'Before meal',
            'start_date': '2024-08-10'
        }

        self.update_drug_url = reverse('medicine', kwargs={'pk': self.medicine1.id})
        response = self.client.put(self.update_drug_url, self.update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine1.refresh_from_db()
        self.assertEqual(self.medicine1.drug_name, self.update_data['drug_name'])
        self.assertEqual(self.medicine1.dosage, self.update_data['dosage'])
        self.assertEqual(self.medicine1.medication_form, self.update_data['medication_form'])
        self.assertEqual(self.medicine1.drug_unit_of_weight, self.update_data['drug_unit_of_weight'])
        self.assertEqual(self.medicine1.no_times, self.update_data['no_times'])
        self.assertEqual(self.medicine1.frequency, self.update_data['frequency'])
        self.assertEqual(self.medicine1.meal_instruction, self.update_data['meal_instruction'])
        # self.assertEqual(str(self.medicine1.start_date), self.update_data['start_date'])

    def test_partial_update_medicine(self):
        self.partial_update_data = {
            'dosage': 300,
            'frequency': 'Weekly'
        }
        response = self.client.patch(reverse('medicine', kwargs={'pk': self.medicine1.id}), self.partial_update_data,
                                     format='json')

        self.medicine1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.medicine1.dosage, self.partial_update_data['dosage'])
        self.assertEqual(self.medicine1.frequency, self.partial_update_data['frequency'])

    def test_retrieve_prescription(self):
        prescription = self.prescription()
        url = reverse('prescription', kwargs={'pk': prescription.data.get('id')})
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['doctor'], prescription.data.get('doctor'))
        self.assertEqual(response.data['patient_firstname'], prescription.data.get('patient_firstname'))
        self.assertEqual(response.data['patient_lastname'], prescription.data.get('patient_lastname'))
        self.assertEqual(len(response.data['prescribed_drugs']), 2)
        self.assertEqual(response.data['prescribed_drugs'][0]['id'], prescription.data.get('prescribed_drugs')[0])

    def test_retrieve_prescription_by_non_owner(self):
        prescription = self.prescription()
        url = reverse('prescription', kwargs={'pk': prescription.data.get('id')})
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), "You do not have permission to access this prescription.")

    def test_destroy_prescription(self):
        prescription = self.prescription()
        url = reverse('prescription', kwargs={'pk': prescription.data.get('id')})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Prescription.objects.filter(id=prescription.data.get('id')).exists())

    def test_create_doctors_note(self):
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\signature.jpg", 'rb') as image:
            signature = image.read()

        doctor_note_data = {
            'doctor': self.doctor.data['id'],
            'patient': self.patient.id,
            'purpose': 'The patient has a medical condition that requires rest and recovery',
            'recommendations': 'Rest and recovery',
            'doctor_signature': SimpleUploadedFile('signatureImage.jpg', signature, 'image/jpg')
        }

        url = reverse('doctors_note')
        response = self.client.post(url, doctor_note_data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorsNote.objects.count(), 2)
        self.assertEqual(self.doctor.data['id'], response.data['doctor'])
        self.assertEqual(self.patient.id, response.data['patient'])
        self.assertEqual(doctor_note_data.get('purpose'), response.data.get('purpose'))
        self.assertEqual(doctor_note_data.get('recommendations'), response.data.get('recommendations'))
        doctor = Doctor.objects.get(id=self.doctor.data.get('id'))
        with open(doctor.signature.path, 'rb') as image:
            doctor_signature = image.read()
            self.assertEqual(doctor_signature, signature)

    def test_update_doctors_note(self):
        doctor = Doctor.objects.get(id=self.doctor.data.get('id'))
        doctor_note = DoctorsNote.objects.create(
            doctor=doctor,
            patient=self.patient,
            purpose="Initial purpose",
            recommendations="Initial recommendations",
            doctor_signature=SimpleUploadedFile('initial_signature.jpg', self.signature, 'image/jpg')
        )
        print(doctor_note.doctor_signature)
        with open(r"C:\Users\ENVY\Desktop\SEMICOLON\updated_signature.jpg", 'rb') as image:
            updated_signature = image.read()

        update_data = {
            'purpose': 'Updated purpose',
            'recommendations': 'Updated recommendations',
            'doctor_signature': SimpleUploadedFile('updated_signature.jpg', updated_signature, 'image/jpg')
        }

        url = reverse('doctors_note-detail', kwargs={'pk': doctor_note.id})
        response = self.client.patch(url, update_data, format='multipart')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doctor_note.refresh_from_db()
        self.assertEqual(doctor_note.purpose, update_data['purpose'])
        self.assertEqual(doctor_note.recommendations, update_data['recommendations'])
        with open(doctor_note.doctor_signature.path, 'rb') as image:
            self.assertEqual(image.read(), updated_signature)

    def test_delete_doctors_note(self):
        url = reverse('doctors_note-detail', kwargs={'pk': self.doctors_note.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DoctorsNote.objects.filter(id=self.doctors_note.id).exists())

    def test_retrieve_doctors_note(self):
        url = reverse('doctors_note-detail', kwargs={'pk': self.doctors_note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['purpose'], self.doctors_note.purpose)
        self.assertEqual(response.data['recommendations'], self.doctors_note.recommendations)

    def test_non_owner_doctor_retrieves_doctors_note(self):
        url = reverse('doctors_note-detail', kwargs={'pk': self.doctors_note.id})
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), "You do not have permission to access this doctor's note.")
