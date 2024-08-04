from rest_framework import serializers

from pharmacies.models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            'id',
            'name',
            'user_profile',
            'phone_number',
            'email',
            'opening_hours',
            'is_open_24_hours',
            'website',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']