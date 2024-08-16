
from users.models import UserProfile, Address
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'phone_number', 'first_name', 'username', 'last_name', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required':True},
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
        return user

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'house_number', 'street', 'city', 'state']
        extra_kwargs = {
            'id': {'read_only': True}
        }
