from django.db.models import Q
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
def has_access_to_appointment(appointment, user):
    is_patient = Patient.objects.filter(user_profile_id=user.id).exists()
    is_doctor = Doctor.objects.filter(user_profile_id=user.id).exists()

    return (is_patient and appointment.patient.user_profile_id == user.id) or (
            is_doctor and appointment.doctor.user_profile_id == user.id)


def doctor_is_available(doctor_id, appointment_date, start_time, end_time):
    doctor = Doctor.objects.filter(id=doctor_id, is_available=True).exists()
    if not doctor:
        return False

    overlapping_appointments = Appointment.appointment_objects.filter(
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        start_time__lt=end_time,  # Start time of existing appointments is before the end time of the new appointment
        end_time__gt=start_time  # End time of existing appointments is after the start time of the new appointment
    ).exists()

    return not overlapping_appointments


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_object(self):
        appointment = super().get_object()
        user = self.request.user
        if has_access_to_appointment(appointment, user):
            return appointment
        else:
            raise PermissionDenied("You do not have permission to view this appointment.")

    def destroy(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        doctor_id = request.data.get("doctor")
        appointment_date = request.data.get("appointment_date")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")
        if start_time is None or end_time is None:
            return Response({"error": "start and end time must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not doctor_is_available(doctor_id, appointment_date, start_time, end_time):
            return Response({"error": "The doctor is not available at this time"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
