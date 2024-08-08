from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from vitals.models import BloodPressure, BloodSugar, HeartRate, BMI, Temperature, Weight, Height, Vitals
from vitals.serializers import BloodPressureSerializer, BloodSugarSerializer, HeartRateSerializer, BMISerializer, \
    TemperatureSerializer, WeightSerializer, HeightSerializer, VitalsSerializer, CreateVitalsSerializer


# Create your views here.

class BloodPressureCreateView(CreateAPIView):
    queryset = BloodPressure.objects.all()
    serializer_class = BloodPressureSerializer


class BloodPressureRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BloodPressure.objects.all()
    serializer_class = BloodPressureSerializer


class BloodSugarViewSet(viewsets.ModelViewSet):
    queryset = BloodSugar.objects.all()
    serializer_class = BloodSugarSerializer


class HeartRateViewSet(viewsets.ModelViewSet):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer


class BMIViewSet(viewsets.ModelViewSet):
    queryset = BMI.objects.all()
    serializer_class = BMISerializer


class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class WeightViewSet(viewsets.ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer


class HeightViewSet(viewsets.ModelViewSet):
    queryset = Height.objects.all()
    serializer_class = HeightSerializer


class VitalsViewSet(viewsets.ModelViewSet):
    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateVitalsSerializer
        return VitalsSerializer
