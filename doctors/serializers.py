from rest_framework import serializers

from doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        user_profile = serializers.PrimaryKeyRelatedField(read_only=True)
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