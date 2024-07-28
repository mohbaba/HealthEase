from django.contrib import admin

from doctors.models import Medicine, Doctor, Prescription, DoctorsNote


# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    pass

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(DoctorsNote)
class DoctorsNotesAdmin(admin.ModelAdmin):
    pass