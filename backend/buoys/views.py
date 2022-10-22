from curses import meta
from datetime import datetime
import re
from urllib import request
from parsers.gyroscopeSensorParser import GyroscopeSensorParser
from parsers.pressureSensorParser import PressureSensorParser
from parsers.sonarSensorParser import SonarSensorParser
from .models import Buoy, Sensor
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch, Q
from urllib.parse import unquote

def get_sensors(request):
    start = unquote(request.query_params['start_date_time']) if 'start_date_time' in request.query_params else datetime.min
    end = unquote(request.query_params['end_date_time']) if 'end_date_time' in request.query_params else datetime.max
    return Sensor.objects.prefetch_related(
        Prefetch('pressure_measurements', queryset=PressureMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_pressure_measurements'),
        Prefetch('light_measurements', queryset=LightMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_light_measurements'),
        Prefetch('buoy_measurements', queryset=BuoyMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_buoy_measurements'),
        Prefetch('echo_measurements', queryset=EchoLocationMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_echo_measurements'),
        Prefetch('sensor_metadata', queryset=SensorMetadata.objects.filter(Q(time_stamp__lte=end)), to_attr='filtered_sensor_metadata')
    )  

class BuoyList(APIView):

    def get(self, request, format=None):
        sensors = get_sensors(request)
        buoys = Buoy.objects.prefetch_related(
            Prefetch('sensors', queryset=sensors)
        )
        print(request.data)
        serializer = BuoySerializer(buoys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuoySerializer(data=request.data)
        if serializer.is_valid():   
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorList(APIView):

    def get(self, request, format=None):
        sensors = get_sensors(request)     
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BuoyDetail(APIView):
    def get(self, request, pk, format=None):
        sensors = get_sensors(request)
        buoys = Buoy.objects.prefetch_related(
            Prefetch('sensors', queryset=sensors)
        )
        buoy = buoys.get(b_id=pk)
        serializer = BuoySerializer(buoy)
        return Response(serializer.data)

class SensorDetail(APIView):
    def get(self, request, pk, format=None):
        sensors = get_sensors(request)
        sensor = sensors.get(s_id=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data)

class LightMeasurementList(APIView):
    
    def get(self, request, format=None):
        light_measurements = LightMeasurement.objects.all()
        serializer = LightMeasurementSerializer(light_measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LightMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuoyMeasurementList(APIView):
    
    def get(self, request, format=None):
        buoy_measurements = BuoyMeasurement.objects.all()
        serializer = BuoyMeasurementSerializer(buoy_measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuoyMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EchoLocationMeasurementList(APIView):
    
    def get(self, request, format=None):
        echo_location_measurements = EchoLocationMeasurement.objects.all()
        serializer = EchoLocationMeasurementSerializer(echo_location_measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EchoLocationMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PressureMeasurementList(APIView):
    
    def get(self, request, format=None):
        echo_location_measurements = PressureMeasurement.objects.all()
        serializer = PressureMeasurementSerializer(echo_location_measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PressureMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuoyUpload(APIView):
    def post(self, request, pk, format=None):
        for key in request.data.keys():
            if key == "metadata":
                file = request.data.get(key)
                headers = [s.strip() for s in file.readline().decode("utf-8").split(",")] + ["time_stamp"]
                values = [s.strip() for s in file.readline().decode("utf-8").split(",")] + [datetime.now()]
                metadataDict = dict(zip(headers, values)) 
                metadataDict["buoy"] = int(pk)
                serializer = BuoyMeasurementSerializer(data=metadataDict)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            if key == "ekkolodd":
                metadata, data = SonarSensorParser().parseFile(request.data.get(key))
                frequency = Sensor.objects.get(s_id=metadata["id"]).s_sample_frequency
                metadata["frequency"] = frequency
                serializer = EchoLocationMeasurementSerializer(data=data, many=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            elif key == "gyroskop":
                metadata, data = GyroscopeSensorParser().parseFile(request.data.get(key))
            elif key == "trykksensor":
                metadata, data = PressureSensorParser().parseFile(request.data.get(key))
                frequency = Sensor.objects.get(s_id=metadata["id"]).s_sample_frequency
                metadata["frequency"] = frequency
                serializer = PressureMeasurementSerializer(data=data, many=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
        return Response(status=status.HTTP_200_OK)