from .models import Buoy, Sensor
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BuoyList(APIView):

    def get(self, request, format=None):
        buoys = Buoy.objects.all()
        serializer = BuoySerializer(buoys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
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
        buoy = Buoy.objects.get(pk=pk)
        serializer = BuoySerializer(buoy, many=True)
        return Response(serializer.data)

class SensorDetail(APIView):
    def get(self, request, pk, format=None):
        sensor = Sensor.objects.get(pk=pk)
        serializer = BuoySerializer(sensor, many=True)
        return Response(serializer.data)