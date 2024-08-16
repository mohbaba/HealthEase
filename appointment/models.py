from django.db import models

from doctors.models import Doctor
from patients.models import Patient


# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField(default=None)
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'),
                                                      ('Cancelled', 'Cancelled')], default='Scheduled')

    class Meta:
        ordering = ['appointment_date']