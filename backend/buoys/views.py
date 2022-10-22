from .models import Buoy, Sensor
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from model_utils.managers import InheritanceManager


class BuoyList(APIView):

    def get(self, request, format=None):
        buoys = Buoy.objects.all()
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
        sensors = Sensor.objects.all()
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
        buoy = Buoy.objects.get(b_id=pk)
        serializer = BuoySerializer(buoy)
        print(serializer.data)
        return Response(serializer.data)

class SensorDetail(APIView):
    def get(self, request, pk, format=None):
        sensor = Sensor.objects.get(s_id=pk)
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