from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacies.models import Pharmacy
from pharmacies.serializers import PharmacySerializer


# Create your views here.

class RegisterPharmacyView(APIView):

    def post(self, request):
        serializer = PharmacySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Pharmacy.objects.create(**serializer.validated_data)
        registration = []
        for pharmacy in Pharmacy.objects.all():
            registration.append(PharmacySerializer(pharmacy).data)
        return Response(registration, status=status.HTTP_201_CREATED)


class UpdatePharmacyView(APIView):
    def put(self, request, pk):
        pharmacy = get_object_or_404(Pharmacy, pk=pk)
        serializer = PharmacySerializer(pharmacy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
