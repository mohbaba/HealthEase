from django.shortcuts import get_object_or_404

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from doctors.models import Doctor
# from doctors.serializers import DoctorSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class DoctorService:
    @staticmethod
    def get_doctor_data(user):
        doctor = get_object_or_404(Doctor, user_profile__id=user.id)
        appointments = Appointment.objects.filter(doctor_id=doctor.id)
        notifications = Notification.objects.filter(recipient__doctor=doctor)

        return {
            # 'doctor': DoctorSerializer(doctor).data,
            'appointments': AppointmentSerializer(appointments, many=True).data,
            'notifications': NotificationSerializer(notifications, many=True).data
        }
