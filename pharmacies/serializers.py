import datetime

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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.opening_hours = validated_data.get('opening_hours', instance.opening_hours)
        instance.is_open_24_hours = validated_data.get('is_open_24_hours', instance.is_open_24_hours)
        instance.website = validated_data.get('website', instance.website)
        instance.save()
        return instance
