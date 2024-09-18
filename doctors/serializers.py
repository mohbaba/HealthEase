import datetime

from rest_framework import serializers

from doctors.models import Doctor, Prescription, Medicine, DoctorsNote
from users.serializers import UserProfileSerializer


class DoctorSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = [
            'id',
            'user_profile',
            'license_number',
            'signature',
            'registration_number',
            'registration_council',
            'registration_year',
            'specialty',
            'consultation_fee',
            'qualification',
            'college',
            'start_year',
            'end_year',
            'is_available',
            'rating'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'signature': {'required': True},
            'license_number': {'write_only': True},
            'rating': {'read_only': True},
        }

    def validate_registration_year(self, value):
        if value > datetime.datetime.year :
            raise serializers.ValidationError("Registration year cannot be in the future.")
        return value


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'drug_name', 'dosage', 'medication_form', 'drug_unit_of_weight', 'start_date', 'no_times',
                  'frequency', 'meal_instruction']
        # read_only_fields = ['id']
        extra_kwargs = {
            'id': {'read_only': True},
            'drug_name': {'required': True},
            'dosage': {'required': True},
            'medication_form': {'required': True},
            'drug_unit_of_weight': {'required': True},
            'no_times': {'required': True},
            'frequency': {'required': True},
            'meal_instruction': {'required': True},
            'start_date': {'required': True},
        }


class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_drugs = MedicineSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'doctor', 'patient_firstname', 'patient_lastname', 'patient_age', 'patient_sex', 'prescribed_date',
            'prescribed_drugs'
        ]
        read_only_fields = ['id', 'prescribed_date']


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = [
            'id', 'doctor', 'patient_firstname', 'patient_lastname', 'patient_age', 'patient_sex',
            'prescribed_date',
            'prescribed_drugs'
        ]
        read_only_fields = ['id', 'prescribed_date']


class DoctorsNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsNote
        fields = ['id', 'doctor', 'patient', 'date_of_issue', 'purpose', 'recommendations', 'doctor_signature']
        read_only_fields = ['id', 'date_of_issue']
