from rest_framework import serializers

from doctors.serializers import MedicineSerializer, DoctorsNoteSerializer
from patients.models import Patient, MedicalRecords


class MedicalRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecords
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    medical_records = serializers.SerializerMethodField()
    newly_prescribed_medicine = serializers.SerializerMethodField()
    doctors_notes = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'medical_records': {'required': False},
            'newly_prescribed_medicine': {'required': False},
            'doctors_notes': {'required': False}
        }
    def get_medical_records(self, obj):
        if obj.medical_records is None:
            return {"default_value": "No medical records available"}
        return MedicalRecordsSerializer(obj.medical_records, many=True).data

    def get_newly_prescribed_medicine(self, obj):
        if obj.newly_prescribed_medicine is None:
            return {"default_value": "No currently prescribed medicine provided yet"}
        return MedicineSerializer(obj.newly_prescribed_medicine, many=True).data

    def get_doctors_notes(self, obj):
        if obj.doctors_notes is None:
            return {"default_value": "No doctors notes provided yet"}
        return DoctorsNoteSerializer(obj.doctors_notes, many=True).data




class PatientRecordsSerializer(serializers.ModelSerializer):
    medical_records = serializers.SerializerMethodField()
    newly_prescribed_medicine = serializers.SerializerMethodField()
    doctors_notes = serializers.SerializerMethodField()

    class Meta:
        model = Patient  # lowercase 'model'
        fields = '__all__'

    def get_medical_records(self, obj):
        if obj.medical_records is None:
            return {"default_value": "No medical records available"}
        return MedicalRecordsSerializer(obj.medical_records, many=True).data

    def get_prescribed_medicine(self, obj):
        if obj.newly_prescribed_medicine is None:
            return {"default_value": "No currently prescribed medicine provided yet"}
        return MedicineSerializer(obj.newly_prescribed_medicine, many=True).data

    def get_doctors_notes(self, obj):
        if obj.doctors_notes is None:
            return {"default_value": "No doctors notes provided yet"}
        return DoctorsNoteSerializer(obj.doctors_notes, many=True).data
