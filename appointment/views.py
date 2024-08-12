from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from doctors.models import Doctor
from patients.models import Patient


# Create your views here.
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_object(self):
        appointment = super().get_object()
        user = self.request.user

        is_patient = Patient.objects.filter(user_profile_id=user.id).exists()
        is_doctor = Doctor.objects.filter(user_profile_id=user.id).exists()

        if is_patient and appointment.patient.user_profile_id == user.id:
            return appointment
        elif is_doctor and appointment.doctor.user_profile_id == user.id:
            return appointment
        else:
            raise PermissionDenied("You do not have permission to view this appointment.")

    def destroy(self, request, *args, **kwargs):
        # Retrieve the appointment object using the same logic as in get_object
        appointment = self.get_object()

        # Only allow deletion if the current user is the patient or the doctor
        user = self.request.user
        if appointment.patient.user_profile_id == user.id or appointment.doctor.user_profile_id == user.id:
            self.perform_destroy(appointment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You do not have permission to delete this appointment.")
