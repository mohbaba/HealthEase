import datetime

from django.db import models
from django.db.models import DO_NOTHING

from patients.models import Patient


# Create your models here.

class BloodPressure(models.Model):
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    last_recorded = models.DateTimeField(auto_now_add=True)


class BloodSugar(models.Model):
    measurement = models.IntegerField(default=0)
    measuring_state = models.CharField(
        choices=[('Fasting', 'Fasting'), ('Before Meal', 'Before Meal'), ('Before Sleep', 'Before Sleep'),
                 ('Before Exercise', 'Before Exercise'),
                 ('After Exercise', 'After Exercise'), ('After Meal', 'After Meal')], max_length=20)
    last_recorded = models.DateTimeField(auto_now_add=True)


class HeartRate(models.Model):
    bpm = models.IntegerField(default=0)
    last_recorded = models.DateTimeField(auto_now_add=True)


class BMI(models.Model):
    bmi = models.IntegerField(default=0)
    last_recorded = models.DateTimeField(auto_now_add=True)


class Temperature(models.Model):
    temperature = models.IntegerField(default=0)
    unit = models.CharField(choices=[('Celcius', 'Celcius'), ('Fahrenheit', 'Fahrenheit')], default='Celcius', max_length=15)
    last_recorded = models.DateTimeField(auto_now_add=True)


class Weight(models.Model):
    weight = models.IntegerField(default=0)
    unit = models.CharField(choices=[('Kilograms', 'Kilograms'), ('Pounds', 'Pounds')], default='Kilograms', max_length=15)
    last_recorded = models.DateTimeField(auto_now_add=True)


class Height(models.Model):
    weight = models.IntegerField(default=0)
    unit = models.CharField(choices=[('Centimeters', 'Centimeters'), ('Inches', 'Inches')], default='Kilograms', max_length=15)
    last_recorded = models.DateTimeField(auto_now_add=True)



class Vitals(models.Model):
    # class VitalObjects(models.Manager):
    #     def get_queryset(self):
    #         return super().get_queryset().filter(patient=self.patient)
    patient = models.ForeignKey(Patient, on_delete=DO_NOTHING)
    weight = models.ForeignKey(Weight, on_delete=DO_NOTHING)
    height = models.ForeignKey(Height, on_delete=DO_NOTHING)
    temperature = models.ForeignKey(Temperature, on_delete=DO_NOTHING)
    bmi = models.ForeignKey(BMI, on_delete=DO_NOTHING)
    heart_rate = models.ForeignKey(HeartRate, on_delete=DO_NOTHING)
    blood_pressure = models.ForeignKey(BloodPressure, on_delete=DO_NOTHING)
    blood_sugar = models.ForeignKey(BloodSugar, on_delete=DO_NOTHING)

    class Meta:
        verbose_name = 'Vitals'
        verbose_name_plural = 'Vitals'

