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
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdatePharmacyView(APIView):
    def put(self, request, pk):
        pharmacy = get_object_or_404(Pharmacy, pk=pk)
        serializer = PharmacySerializer(pharmacy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeletePharmacyView(APIView):
    def delete(self, request, pk):
        pharmacy = get_object_or_404(Pharmacy, pk=pk)
        pharmacy.delete()
        return Response(data={'message': 'Pharmacy deleted!'}, status=status.HTTP_200_OK)


class ListPharmacyView(APIView):
    def get(self, request):
        pharmacies = Pharmacy.objects.all()
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrievePharmacyView(APIView):
    def get(self, request, pk):
        pharmacy = get_object_or_404(Pharmacy, pk=pk)
        serializer = PharmacySerializer(pharmacy)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterListPharmacyView(APIView):
    def get(self, request):
        pharmacies = Pharmacy.objects.all()
        name = request.query_params.get('name', None)
        if name:
            pharmacies = pharmacies.filter(name__icontains=name)
        serializer = PharmacySerializer(pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
