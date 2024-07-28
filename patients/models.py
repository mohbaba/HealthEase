from datetime import datetime

from django.db import models
from django.db.models import CASCADE

from doctors.models import Medicine, DoctorsNote, DRUGS
from users.models import UserProfile

# Create your models here.


ALLERGIES = [
    ('Lactose', 'Lactose'),
    ('Soy', 'Soy'),
    ('Seafood', 'Seafood'),
    ('Nuts', 'Nuts'),
    ('Eggs', 'Eggs'),
    ('Fish', 'Fish')
]


DISEASES = [
    ('Diabetes', 'Diabetes'),
    ('Hypertension', 'Hypertension'),
    ('PCOS', 'PCOS'),
    ('Hypothyroidism', 'Hypothyroidism'),
    ('COPD', 'COPD'),
    ('Asthma', 'Asthma')
]

INCIDENT = [
    ('Burns', 'Burns'),
    ('Spinal Cord Injury', 'Spinal Cord Injury'),
    ('Spinal Fracture', 'Spinal Fracture'),
    ('Skull Fracture', 'Skull Fracture'),
]

SURGERIES = [
    ('Heart', 'HEART'),
    ('Liver', 'LIVER'),
    ('Kidney', 'KIDNEY'),
    ('Lungs', 'LUNGS'),
    ('Brain', 'BRAIN'),
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
    medical_records = models.ForeignKey(MedicalRecords, on_delete=CASCADE)
    newly_prescribed_medicine = models.ManyToManyField(Medicine)
    doctors_notes = models.ManyToManyField(DoctorsNote,related_name='notes')

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.user_profile.get_full_name()
