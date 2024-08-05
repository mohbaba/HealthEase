import datetime

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.models import Doctor, Medicine, Prescription
from doctors.serializers import DoctorSerializer, MedicineSerializer, PrescriptionSerializer
from patients.models import Patient
from users.models import UserProfile


# Create your views here.

class RegisterDoctorView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.errors)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class PrescribeMedicineView(APIView):
    def post(self, request):
        data = request.data

        doctor = get_object_or_404(Doctor, id=data.get('doctor'))
        patient = get_object_or_404(Patient, id=data.get('patient'))

        # Validate and process prescribed drugs data
        prescribed_drugs_data = data.get('prescribed_drugs')
        drugs = []

        for drug_data in prescribed_drugs_data:
            drug_serializer = MedicineSerializer(data=drug_data)
            if drug_serializer.is_valid():
                drug = drug_serializer.save()
                drugs.append(drug)
            else:
                return Response(drug_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the prescription
        prescription_data = {
            'doctor': doctor.id,
            'patient_firstname': patient.user_profile.first_name,
            'patient_lastname': patient.user_profile.last_name,
            'patient_age': 30, #Remember to fix this when changed
            'patient_sex': 'Male', #This too
            'prescribed_date': datetime.datetime.now(),
            'prescribed_drugs': [drug.id for drug in drugs]
        }

        prescription_serializer = PrescriptionSerializer(data=prescription_data)

        if prescription_serializer.is_valid():
            prescription_serializer.save()
            return Response(prescription_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(prescription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineView(APIView):

    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
