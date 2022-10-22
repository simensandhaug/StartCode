from copyreg import constructor
from dataclasses import field
from rest_framework import serializers
from .models import *

        
class SensorSerializer(serializers.ModelSerializer):
    
    measurements = serializers.SerializerMethodField()
    
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def create(self, data):
        return Sensor.objects.create(**data)
    
    def get_measurements(self, obj):
        match obj.s_type:
            case "light" :
                return LightMeasurement.objects.filter(sensor=obj.s_id)
            case "buoy":
                return BuoyMeasurement.objects.filter(sensor=obj.s_id)
            case "echo":
                return EchoLocationMeasurement.objects.filter(sensor=obj.s_id)
    
class BuoySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Buoy
        fields = '__all__'
    
    def create(self, data):
        print(data)
        return Buoy.objects.create(**data)
        
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