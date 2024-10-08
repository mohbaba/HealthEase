from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, \
    ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from doctors.models import Doctor, Medicine, Prescription, DoctorsNote
from doctors.serializers import DoctorSerializer, MedicineSerializer, PrescriptionSerializer, DoctorsNoteSerializer, \
    PrescriptionCreateSerializer
from patients.models import Patient


# Create your views here.

class DoctorCreate(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        specialty = self.request.query_params.get('specialty',None)
        name = self.request.query_params.get('name', None)
        rating = self.request.query_params.get('rating', None)
        consultation_fee = self.request.query_params.get('fee', None)
        is_available = self.request.query_params.get('available', None)

        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)

        if name:
            queryset = queryset.filter(user_profile__first_name__icontains=name) | queryset.filter(
                user_profile__last_name__icontains=name)

        if rating:
            queryset = queryset.filter(rating=rating)

        if consultation_fee:
            queryset = queryset.filter(consultation_fee__lte=consultation_fee)

        if is_available:
            queryset = queryset.filter(is_available=is_available)

        return queryset

class DoctorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


# class DoctorListView(ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer


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
            'patient_age': date.today().year - patient.date_of_birth.year,
            'patient_sex': patient.user_profile.gender,
            'prescribed_date': datetime.now(),
            'prescribed_drugs': [drug.id for drug in drugs]
        }

        prescription_serializer = PrescriptionCreateSerializer(data=prescription_data)

        if prescription_serializer.is_valid():
            prescription_serializer.save()
            return Response(prescription_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(prescription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineView(CreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class MedicineRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class PrescriptionRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    # permission_classes = [IsAuthenticated]

    def get_object(self):
        prescription = super().get_object()
        doctor = Doctor.objects.filter(user_profile=self.request.user.id).first()

        if doctor is None or prescription.doctor.id != doctor.id:
            raise PermissionDenied(detail="You do not have permission to access this prescription.")

        return prescription


class DoctorsNoteCreate(CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsNoteSerializer


class DoctorsNoteRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = DoctorsNote.objects.all()
    serializer_class = DoctorsNoteSerializer

    def get_object(self):
        doctor_note = super().get_object()
        doctor = Doctor.objects.filter(user_profile=self.request.user.id).first()

        if doctor is None or doctor_note.doctor.id != doctor.id:
            raise PermissionDenied(detail="You do not have permission to access this doctor's note.")

        return doctor_note
