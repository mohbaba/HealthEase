from datetime import datetime

from django.db import models
from django.db.models import CASCADE

from users.models import UserProfile

# Create your models here.
DRUGS = [
    ('21st Century fish oil', '21st Century fish oil'),
    ('Abidec', 'Abidec'),
    ('Accord Bendroflumethiazide', 'Accord Bendroflumethiazide'),
    ('ACCULOL', 'ACCULOL'),
    ('Actavis Doxycycline', 'Actavis Doxycycline'),
    ('Actinaza', 'Actinaza'),
    ('Aday kit tablets', 'Aday kit tablets'),
    ('Afrab vite', 'Afrab vite'),
    ('Africolo 1000 Capsules', 'Africolo 1000 Capsules')
]


ALLERGIES = [
    ('Lactose', 'Lactose'),
    ('Soy', 'Soy'),
    ('Seafood', 'Seafood'),
    ('Nuts', 'Nuts'),
    ('Eggs', 'Eggs'),
    ('Fish', 'Fish'),
    ('None', 'NONE'),
    ('Other', 'OTHER'),
]

DISEASES = [
    ('Diabetes', 'Diabetes'),
    ('Hypertension', 'Hypertension'),
    ('PCOS', 'PCOS'),
    ('Hypothyroidism', 'Hypothyroidism'),
    ('COPD', 'COPD'),
    ('Asthma', 'Asthma'),
    ('None', 'NONE'),
    ('Other', 'OTHER'),
]

INCIDENT = [
    ('Burns', 'Burns'),
    ('Spinal Cord Injury', 'Spinal Cord Injury'),
    ('Spinal Fracture', 'Spinal Fracture'),
    ('Skull Fracture', 'Skull Fracture'),
    ('None', 'NONE'),
    ('Other', 'OTHER'),
]

SURGERIES = [
    ('Heart', 'HEART'),
    ('Liver', 'LIVER'),
    ('Kidney', 'KIDNEY'),
    ('Lungs', 'LUNGS'),
    ('Brain', 'BRAIN'),
    ('None', 'NONE'),
    ('Other', 'OTHER'),
]

SMOKING_HABIT = [
    ('I dont smoke', 'NOT_SMOKER'),
    ("I used to, but I've quit", 'NO_LONGER_SMOKER'),
    ('1 or more times per day', "SMOKES")
]

ALCOHOL_HABIT = [
    ('Non-drinker', 'NON-DRINKER'),
    ('Rare', 'RARE'),
    ('Social', 'SOCIAL'),
    ('Regular', 'REGULAR'),
    ('Heavy', 'HEAVY')
]

LIFESTYLE = [
    ('Sedentary (low)', 'LOW'),
    ('Moderately active', 'MODERATELY'),
    ('Active (high)', 'HIGH'),
    ('Athletic (very high)', 'VERY HIGH'),
]

FOOD_PREFERENCES = [
    ('Vegetarian', 'VEGETARIAN'),
    ('Non-Vegetarian', 'NON-VEGETARIAN'),
    ('Eggetarian', 'EGGETARIAN'),
    ('Vegan', 'VEGAN')
]

BLOOD_GROUP = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')
]

GENOTYPE = [
    ('AA', 'AA'),
    ('AC', 'AC'),
    ('SS', 'SS'),
    ('SC', 'SC'),
    ('AS', 'AS'),
]


class MedicalRecords(models.Model):
    allergies = models.CharField(choices=ALLERGIES, max_length=100)
    current_medications = models.CharField(choices=DRUGS, max_length=100)
    past_medications = models.CharField(choices=DRUGS, max_length=100)
    chronic_disease = models.CharField(choices=DISEASES, max_length=100)
    incident = models.CharField(choices=INCIDENT, max_length=100)
    surgeries = models.CharField(choices=SURGERIES, max_length=100)
    smoking_habit = models.CharField(choices=SMOKING_HABIT, max_length=100)
    alcohol_habit = models.CharField(choices=ALCOHOL_HABIT, max_length=100)
    lifestyle = models.CharField(choices=LIFESTYLE, max_length=100)
    food_preferences = models.CharField(choices=FOOD_PREFERENCES, max_length=100)

    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

    def __str__(self):
        return self.id


class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='patient')
    medical_records = models.ForeignKey(MedicalRecords, on_delete=CASCADE, null=True, blank=True, default='null')
    newly_prescribed_medicine = models.ManyToManyField('doctors.Medicine', blank=True, null=True, default='null')
    doctors_notes = models.ManyToManyField('doctors.DoctorsNote', related_name='notes', blank=True, null=True, default='null')
    date_of_birth = models.DateField(null=True, blank=True, default='Not specified yet')
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=5, blank=True)
    genotype = models.CharField(choices=GENOTYPE, max_length=10, blank=True)
    # TODO: might have to make emergency contact into a model
    emergency_contact_name = models.CharField(max_length=40, default='None')
    emergency_contact_phone = models.CharField(max_length=13, default='+23480000000')

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.user_profile.get_full_name()
