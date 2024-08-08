from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class RegisterPatientView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_profile_id = request.data.get('user_profile')
