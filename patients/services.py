from django.shortcuts import get_object_or_404

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from patients.models import Patient
from users.models import UserProfile
from vitals.models import Vitals
from vitals.serializers import VitalsSerializer


class PatientService:
    @staticmethod
    def get_patient_data(user):
        from patients.serializers import PatientSerializer
        patient = get_object_or_404(Patient, user_profile__id=user.id)
        appointments = Appointment.objects.filter(patient=patient)
        vitals = Vitals.objects.filter(patient=patient)
        return {
            'patient_details': PatientSerializer(patient).data,
            'appointments': AppointmentSerializer(appointments, many=True).data,
            'vitals': VitalsSerializer(vitals, many=True).data
        }
