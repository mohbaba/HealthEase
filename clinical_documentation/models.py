import datetime

from django.db import models
from django.utils import timezone
# from django.apps import


# Create your models here.

class ClinicalNote(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    subjective = models.TextField()  # Patient's reported symptoms, medical history
    objective = models.TextField()  # Doctor's observations, physical exam results
    assessment = models.TextField()  # Doctor's diagnosis or differential diagnosis
    plan = models.TextField()  # Treatment plan, prescriptions, follow-up

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"Clinical Note for {self.patient} by {self.doctor} on {self.date_created.strftime('%Y-%m-%d')}"


class LabTestRequest(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)

    # Details of the lab test request
    test_name = models.CharField(max_length=255)  # Name of the test requested
    clinical_information = models.TextField()  # Reason for the test or relevant symptoms
    specimen_type = models.CharField(max_length=100)  # Type of sample required (e.g., Blood, Urine)
    icd_code = models.CharField(max_length=10, blank=True, null=True)  # Optional diagnosis code

    class Meta:
        ordering = ['-date_requested']

    def __str__(self):
        return f"Lab Test Request: {self.test_name} for {self.patient} by {self.doctor}"
