from django.db import models

from django.db.models import DO_NOTHING
from django.apps import apps

# from patients.models import MedicalRecords
# from patients.models import Patient
from users.models import UserProfile

# Create your models here.

RATING = [
    (0, 'ZERO_STAR'),
    (1, 'ONE_STAR'),
    (2, 'TWO_STAR'),
    (3, 'THREE_STAR'),
    (4, 'FOUR_STAR'),
    (5, 'FIVE_STAR'),
]
SPECIALTY = [
    ('ALLERGY_AND_IMMUNOLOGY', 'Allergy and Immunology'),
    ('ANESTHESIOLOGY', 'Anesthesiology'),
    ('CARDIOLOGY', 'Cardiology'),
    ('DERMATOLOGY', 'Dermatology'),
    ('EMERGENCY_MEDICINE', 'Emergency Medicine'),
    ('FAMILY_MEDICINE', 'Family Medicine'),
    ('INTERNAL_MEDICINE', 'Internal Medicine'),
    ('MEDICAL_GENETICS', 'Medical Genetics'),
    ('NEUROLOGY', 'Neurology'),
    ('NUCLEAR_MEDICINE', 'Nuclear Medicine'),
    ('OBSTETRICS_AND_GYNAECOLOGY', 'Obstetrics and Gynaecology'),
    ('OPHTHALMOLOGY', 'Ophthalmology'),
    ('PATHOLOGY', 'Pathology'),
    ('PAEDIATRICS', 'Paediatrics'),
    ('PSYCHIATRY', 'Psychiatry'),
    ('SURGERY', 'Surgery'),
    ('UROLOGY', 'Urology'),
]


# 1. Remember to put image field for the picture of the license, certificates and other crucial credentials for registration
# 2. Validate phone numbers, emails and license numbers
# 3. Make all fields required
class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor')
    license_number = models.IntegerField()
    signature = models.ImageField()
    registration_number = models.IntegerField()
    registration_council = models.CharField(max_length=50)
    registration_year = models.DateField(auto_now=False)
    rating = models.IntegerField(choices=RATING, default='ZERO_STAR')
    specialty = models.CharField(choices=SPECIALTY, max_length=100)
    consultation_fee = models.IntegerField()
    qualification = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    start_year = models.DateField(auto_now=False)
    end_year = models.DateField(auto_now=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return self.user_profile.get_full_name()


SEX = [
    ('Male', 'MALE'),
    ('Female', 'FEMALE')
]

DRUG_UNIT_OF_WEIGHT = [
    ('mg', 'MILLIGRAMS'),
    ('mcg', 'MICROGRAMS'),
    ('mcg', 'MICROGRAMS'),
    ('ng', 'NANOGRAMS'),
    ('pg', 'PICOGRAMS'),
    ('pg', 'PICOGRAMS'),
    ('ml', 'MILLILITRES'),
    ('microlitres', 'MICROLITRES'),
]

MEDICATION_FORM = [
    ('Tablet', 'TABLET'),
    ('Capsule', 'CAPSULE'),
    ('Liquid', 'LIQUID'),
    ('Topical', 'TOPICAL'),
    ('Drops', 'DROPS'),
    ('Foam', 'FOAM'),
    ('Spray', 'SPRAY'),
    ('Powder', 'POWDER'),
    ('Injection', 'INJECTION'),
    ('Patch', 'PATCH'),
    ('Cream', 'CREAM'),
    ('Lotion', 'LOTION'),
]

FREQUENCY = [
    ('Daily', 'DAILY'),
    ('Weekly', 'WEEKLY'),
    ('Monthly', 'MONTHLY'),
    ('Twice a week', 'TWICE_A_WEEK'),
    ('Alternative days', 'ALTERNATIVE_DAYS'),
    ('Every fortnight', 'FORTNIGHT'),
]

MEAL_INSTRUCTION = [
    ('Before meal', 'BEFORE_MEAL'),
    ('With meal', 'WITH_MEAL'),
    ('In between meal', 'INBETWEEN_MEAL'),
    ('After meal', 'AFTER_MEAL'),
    ('Empty stomach', 'EMPTY_STOMACH'),
    ('Before sleep', 'BEFORE_SLEEP'),
]



class Medicine(models.Model):
    #We'll use these drugs pending the time we find an api for it
    # medicine_name = models.CharField(choices=DRUGS, max_length=50)
    medication_form = models.CharField(choices=MEDICATION_FORM, max_length=50)
    dosage = models.IntegerField(default=0)
    no_times = models.IntegerField(default=1)
    frequency = models.CharField(choices=FREQUENCY, max_length=50)
    meal_instruction = models.CharField(choices=MEAL_INSTRUCTION, max_length=100)
    start_date = models.DateField(auto_now_add=True)
    drug_name = models.CharField(max_length=100)
    drug_unit_of_weight = models.CharField(choices=DRUG_UNIT_OF_WEIGHT, max_length=100)

    class Meta:
        verbose_name = 'Medicine'
        verbose_name_plural = 'Drugs'

    def __str__(self):
        return self.drug_name


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=DO_NOTHING)
    patient_firstname = models.CharField(max_length=100)
    patient_lastname = models.CharField(max_length=100)
    patient_age = models.IntegerField(default=0)
    patient_sex = models.CharField(choices=SEX, max_length=10)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    # dosage = models.IntegerField()
    prescribed_drugs = models.ManyToManyField(Medicine, related_name='patients_prescribed_drugs')

    # no_times = models.IntegerField(default=1)
    # frequency = models.CharField(choices=FREQUENCY, max_length=50)
    # meal_instruction = models.CharField(choices=MEAL_INSTRUCTION, max_length=100)
    # start_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'

    def __str__(self):
        return f"Prescribed by Dr. {self.doctor.user_profile.get_full_name()} to {self.patient_firstname} {self.patient_lastname}"


class DoctorsNote(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=DO_NOTHING)
    patient = models.ForeignKey('patients.Patient', on_delete=DO_NOTHING)

    purpose = models.TextField()
    recommendations = models.TextField(blank=True, null=True)
    # note_status = models.CharField(max_length=20, choices=[('Issued', 'Issued'), ('Revoked', 'Revoked')],
    #                                default='Issued')
    # verification_code = models.CharField(max_length=100, unique=True)
    date_of_issue = models.DateField(auto_now_add=True)
    doctor_signature = models.ImageField()

    class Meta:
        verbose_name = 'Doctor\'s Note'
        verbose_name_plural = 'Doctor\'s Notes'
        ordering = ['-date_of_issue']

    def get_patient(self):
        Patient = apps.get_model('patients', 'Patient')
        return Patient.objects.get(id=self.patient_id)

    def __str__(self):
        return f"Doctor's Note for {self.get_patient()} by {self.doctor.user_profile.get_full_name()} on {self.date_of_issue}"
