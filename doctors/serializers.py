import datetime
from time import timezone

from rest_framework import serializers

from doctors.models import Doctor
from users.serializers import UserProfileSerializer


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        user_profile = UserProfileSerializer(read_only=True)
        model = Doctor
        fields = [
            'user_profile',
            'license_number',
            'signature',
            'registration_number',
            'registration_council',
            'registration_year',
            'rating',
            'specialty',
            'consultation_fee',
            'qualification',
            'college',
            'start_year',
            'end_year',
            'is_available'
        ]
        extr_kwargs = {
            'signature': {'required': True}
        }

        def validate_registration_year(self, value):
            if value > datetime.datetime.now():
                raise serializers.ValidationError("Registration year cannot be in the future.")
            return value
