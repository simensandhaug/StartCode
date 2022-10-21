from dataclasses import field
from rest_framework import serializers
from .models import *

class BuoySerializer(serializers.Serializer):
    b_id = serializers.IntegerField()
    class Meta:
        model = Buoy
        fields = '__all__'
    
    def create(self, data):
        print(data)
        return Buoy.objects.create(**data)
        
class SensorSerializer(serializers.Serializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def create(self, data):
        return Sensor.objects.create(**data)
        
class MeasurementSerializer(serializers.Serializer):
    class Meta:
        model = Measurement
        fields = '__all__'
        
    def create(self, data):
        return Measurement.objects.create(**data)

class LightMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = LightMeasurement
        fields = '__all__'
        
    def create(self, data):
        return LightMeasurement.objects.create(**data)
        
class EchoLocationMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = EchoLocationMeasurement
        fields = '__all__'
        
    def create(self, data):
        return EchoLocationMeasurement.objects.create(**data)
        
class BuoyMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = BuoyMeasurement
        fields = '__all__'
        
    def create(self, data):
        return BuoyMeasurement.objects.create(**data)