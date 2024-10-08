from rest_framework import serializers

from appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'status', 'reason', 'status', 'start_time', 'end_time']
