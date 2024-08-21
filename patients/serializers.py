from rest_framework import serializers

from doctors.serializers import MedicineSerializer, DoctorsNoteSerializer
from patients.models import Patient, MedicalRecords


class MedicalRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecords
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'medical_records': {'required': False},
            'newly_prescribed_medicine': {'required': False},
            'doctors_notes': {'required': False}
        }

    medical_records = MedicalRecordsSerializer()
    newly_prescribed_medicine = MedicineSerializer(many=True)
    doctors_notes = DoctorsNoteSerializer(many=True)


class PatientRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Patient
        fields = '__all__'

    medical_records = MedicalRecordsSerializer()
    newly_prescribed_medicine = MedicineSerializer()
    doctors_notes = DoctorsNoteSerializer()
