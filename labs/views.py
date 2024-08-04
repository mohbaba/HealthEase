from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lab
from .serializers import LabSerializer
from rest_framework import filters


class LabListCreateView(generics.ListCreateAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabListFilterByName(generics.ListCreateAPIView):
    serializer_class = LabSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Lab.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
            return Response(data=queryset, status=status.HTTP_200_OK)


class LabListFilterByLocation(generics.ListCreateAPIView):
    serializer_class = LabSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'location']
    ordering = ['name']

    def get_queryset(self):
        queryset = Lab.objects.all()
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return Response(data=queryset, status=status.HTTP_200_OK)


class DeleteLab(APIView):
    def delete(self, request, pk):
        lab = get_object_or_404(Lab, pk=pk)
        lab.delete()
        return Response(data={'message': 'Lab deleted successfully!'}, status=status.HTTP_200_OK)
