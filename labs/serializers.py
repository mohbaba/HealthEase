from rest_framework import serializers
from .models import Lab


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = [
            'name',
            'location',
            'established_date',
            'description',
            'contact_number',
            'email',
            'is_active'
        ]
