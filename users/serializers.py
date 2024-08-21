from django.contrib.auth import authenticate
from djoser.serializers import TokenCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from doctors.services import DoctorService
from patients.models import Patient
from patients.services import PatientService
from users.models import Address
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'phone_number', 'first_name', 'username', 'last_name', 'password', 'role', 'gender']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
            'phone_number': {'required': True},

        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError({"password": "This field is required."})
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        if user.role == 'PATIENT':
            patient = Patient(user_profile=user)
            patient.save()
        return user


class UserCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        refresh_token = RefreshToken.for_user(user)
        data['refresh_token'] = str(refresh_token)
        data['user'] = UserProfileSerializer(user).data
        data.pop('password')
        data.pop('email')
        if user.role == 'PATIENT':
            data.update(PatientService.get_patient_data(user))
        elif user.role == 'DOCTOR':
            data['doctor'] = DoctorService.get_doctor_data(user)
        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'house_number', 'street', 'city', 'state']
        extra_kwargs = {
            'id': {'read_only': True}
        }
