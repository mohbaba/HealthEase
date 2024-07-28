from django.db import models

# Create your models here.

class Appointment(models.Model):
    appointment_time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)
    appointment_date = models.DateField(auto_now_add=True)