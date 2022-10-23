from rest_framework import serializers
from .models import *

""" class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields """

        

        
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
        
    def create(self, data):
        return LightMeasurement.objects.create(**data)
        
class EchoLocationMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EchoLocationMeasurement
        fields = '__all__'
        
    def create(self, data):
        return EchoLocationMeasurement.objects.create(**data)

class PressureMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureMeasurement
        fields = '__all__'
                
    def create(self, data):
        return PressureMeasurement.objects.create(**data)
        
class GyroscopeMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GyroscopeMeasurement
        fields = '__all__'
                
    def create(self, data):
        return GyroscopeMeasurement.objects.create(**data)

class BuoyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuoyMeasurement
        fields = '__all__'
        
    def create(self, data):
        return BuoyMeasurement.objects.create(**data)
    
class SensorMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorMetadata
        fields = '__all__'
        
    def create(self, data):
        return SensorMetadata.objects.create(**data)
    
class SensorSerializer(serializers.ModelSerializer):
    
    pressure_measurements = PressureMeasurementSerializer(read_only=True, many=True, source='filtered_pressure_measurements')
    light_measurements = LightMeasurementSerializer(read_only=True, many=True, source='filtered_light_measurements')
    echo_measurements = EchoLocationMeasurementSerializer(read_only=True, many=True, source='filtered_echo_measurements')
    gyro_measurements = GyroscopeMeasurementSerializer(read_only=True, many=True, source='filtered_gyro_measurements')
    
    sensor_metadata = SensorMetadataSerializer(read_only=True, many=True, source='filtered_sensor_metadata')
    
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def create(self, data):
        return Sensor.objects.create(**data)
    

class BuoySerializer(serializers.ModelSerializer):
    
    sensors = SensorSerializer(read_only=True, many=True)
    buoy_measurements = BuoyMeasurementSerializer(read_only=True, many=True, source='filtered_buoy_measurements')   

    
    class Meta:
        model = Buoy
        fields = '__all__'
    
    def create(self, data):
        print(data)
        return Buoy.objects.create(**data)
    