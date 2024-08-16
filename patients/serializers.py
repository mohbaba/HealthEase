from rest_framework import serializers

from patients.models import Patient
from users.serializers import UserProfileSerializer


class PatientSerializer(serializers.ModelSerializer):
    # user_profile = UserProfileSerializer()
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'medical_records': {'required': False},
            'newly_prescribed_medicine': {'required': False},
            'doctors_notes': {'required': False}
        }
