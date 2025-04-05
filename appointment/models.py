from django.db import models

from doctors.models import Doctor
from patients.models import Patient


# Create your models here.

class Appointment(models.Model):
    class AppointmentObjects(models.Manager):

        def get_queryset(self):

            return super().get_queryset().filter(status='Scheduled')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_date = models.DateField()
    reason = models.TextField(default=None)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'),
                                                      ('Cancelled', 'Cancelled')], default='Scheduled')
    appointment_objects = AppointmentObjects()
    objects = models.Manager()

    class Meta:
        ordering = ['appointment_date']
