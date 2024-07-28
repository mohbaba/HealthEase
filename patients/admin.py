from django.contrib import admin

from patients.models import MedicalRecords


# Register your models here.

@admin.register(MedicalRecords)
class MedicalRecordsAdmin(admin.ModelAdmin):
    pass