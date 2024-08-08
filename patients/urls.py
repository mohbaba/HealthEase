from django.urls import path

from patients.views import RegisterPatientView

urlpatterns = [
    path('auth/registerPatient/', RegisterPatientView.as_view(), name='register_patient')
]
