from django.shortcuts import render, get_object_or_404
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer
from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserCreateSerializer


# Create your views here.

class UserRegistration(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomTokenCreateView(TokenCreateView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
