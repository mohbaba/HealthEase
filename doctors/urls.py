from django.urls import path

from doctors.views import RegisterDoctorView, PrescribeMedicineView, MedicineView

urlpatterns = [
    path('auth/registerDoctor/', RegisterDoctorView.as_view(), name='register_doctor'),
    path('prescribeMedicine', PrescribeMedicineView.as_view(), name='prescribe'),
    path('addDrug', MedicineView.as_view(), name='add-drug')
]