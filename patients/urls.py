from django.urls import path

from patients.views import PatientRegistration

urlpatterns = [
    path('auth/registerPatient/', PatientRegistration.as_view(), name='register_patient')
]
