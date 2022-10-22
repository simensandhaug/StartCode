from copyreg import constructor
from dataclasses import field
from multiprocessing import context
from rest_framework import serializers
from .models import *

""" class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields """

        
class SensorSerializer(serializers.ModelSerializer):
    
    measurements = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def create(self, data):
        print(data)
        return Sensor.objects.create(**data)
    
    def get_measurements(self, obj):
        print(obj)
        match obj.s_type:
            case "light" :
                return LightMeasurementSerializer(LightMeasurement.objects.filter(sensor=obj.s_id)).data
            case "buoy":
                return BuoyMeasurement.objects.filter(sensor=obj.s_id).data
            case "echo":
                return EchoLocationMeasurement.objects.filter(sensor=obj.s_id).data
    
class BuoySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Buoy
        fields = '__all__'
    
    def create(self, data):
        print(data)
        return Buoy.objects.create(**data)
        
# class MeasurementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Measurement
#         fields = '__all__'
        
#     def create(self, data):
#         return Measurement.objects.create(**data)

class LightMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightMeasurement
        fields = '__all__'
        extra_fields = ['sensor', 'time_stamp']
        
    def create(self, data):
        return LightMeasurement.objects.create(**data)
        
class EchoLocationMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchoLocationMeasurement
        fields = '__all__'
        extra_fields = ['sensor', 'time_stamp']
        
    def create(self, data):
        return EchoLocationMeasurement.objects.create(**data)
        
class BuoyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuoyMeasurement
        fields = '__all__'
        extra_fields = ['sensor', 'time_stamp']
        
    def create(self, data):
        return BuoyMeasurement.objects.create(**data)