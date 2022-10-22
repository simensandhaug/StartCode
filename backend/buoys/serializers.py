from dataclasses import field
from rest_framework import serializers
from .models import *

class BuoySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buoy
        fields = '__all__'
    
    def create(self, data):
        print(data)
        return Buoy.objects.create(**data)
        
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def create(self, data):
        return Sensor.objects.create(**data)
        
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'
        
    def create(self, data):
        return Measurement.objects.create(**data)

class LightMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightMeasurement
        fields = '__all__'
        
    def create(self, data):
        return LightMeasurement.objects.create(**data)
        
class EchoLocationMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchoLocationMeasurement
        fields = '__all__'
        
    def create(self, data):
        return EchoLocationMeasurement.objects.create(**data)
        
class BuoyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuoyMeasurement
        fields = '__all__'
        
    def create(self, data):
        return BuoyMeasurement.objects.create(**data)