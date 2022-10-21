from dataclasses import field
from rest_framework import serializers
from .models import *

class BouySerializer(serializers.Serializer):
    class Meta:
        model = Bouy
        fields = '__all__'
        
class SensorSerializer(serializers.Serializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
class MeasurementSerializer(serializers.Serializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class LightMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = LightMeasurement
        fields = '__all__'
        
class EchoLocationMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = EchoLocationMeasurement
        fields = '__all__'
        
class BouyMeasurementSerializer(serializers.Serializer):
    class Meta:
        model = BouyMeasurement
        fields = '__all__'