from rest_framework import serializers

from patients.models import Patient
from vitals.models import BloodPressure, Vitals, Height, Weight, Temperature, BMI, HeartRate, BloodSugar


class BloodPressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodPressure
        fields = ['systolic', 'diastolic', 'last_recorded']
        read_only_fields = ['last_recorded']


class BloodSugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodSugar
        fields = '__all__'
        read_only_fields = ['last_recorded']


class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = '__all__'
        read_only_fields = ['last_recorded']


class BMISerializer(serializers.ModelSerializer):
    class Meta:
        model = BMI
        fields = '__all__'
        read_only_fields = ['last_recorded']


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = '__all__'
        read_only_fields = ['last_recorded']


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = '__all__'
        read_only_fields = ['last_recorded']


class HeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Height
        fields = '__all__'
        read_only_fields = ['last_recorded']


class CreateVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = '__all__'


class VitalsSerializer(serializers.ModelSerializer):
    blood_pressure = BloodPressureSerializer(many=False, required=False)
    weight = WeightSerializer()
    height = HeightSerializer()
    bmi = BMISerializer()
    heart_rate = HeartRateSerializer()
    blood_sugar = BloodSugarSerializer()
    temperature = TemperatureSerializer()
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vitals
        fields = '__all__'

    def update(self, instance, validated_data):
        nested_fields = ['weight', 'height', 'bmi', 'heart_rate', 'blood_pressure', 'blood_sugar', 'temperature']
        for field in nested_fields:
            if field in validated_data:
                nested_data = validated_data.pop(field)
                nested_instance = getattr(instance, field)
                for attr, value in nested_data.items():
                    setattr(nested_instance, attr, value)
                nested_instance.save()

        return super().update(instance, validated_data)