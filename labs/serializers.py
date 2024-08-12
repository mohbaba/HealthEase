from rest_framework import serializers
from .models import Lab


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = [
            'id',
            'name',
            'user_profile',
            'location',
            'description',
            'contact_phone',
            'contact_email',
            'opening_hours',
            'equipment_list',
            'capacity',
            'date_established'
        ]
        read_only_fields = ['id']
