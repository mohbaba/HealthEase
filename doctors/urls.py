from django.urls import path

from doctors.views import RegisterDoctorView

urlpatterns = [
    path('auth/registerDoctor/', RegisterDoctorView.as_view(), name='register_doctor')
]