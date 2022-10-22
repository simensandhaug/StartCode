from datetime import datetime
import re
from urllib import request
from .models import Buoy, Sensor
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch, Q
from urllib.parse import unquote

def get_sensors(request):
    start = request.query_params['start_date_time'] if 'start_date_time' in request.query_params else datetime.min
    end = request.query_params['end_date_time'] if 'end_date_time' in request.query_params else datetime.max
    start = unquote(start)
    end = unquote(end)
    print(start, end)
    return Sensor.objects.prefetch_related(
        Prefetch('light_measurements', queryset=LightMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_light_measurements'),
        Prefetch('buoy_measurements', queryset=BuoyMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_buoy_measurements'),
        Prefetch('echo_measurements', queryset=EchoLocationMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_echo_measurements')
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