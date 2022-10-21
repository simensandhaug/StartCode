import models
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Bouys(APIView):

    def get(self, request, format=None):
        bouys = models.Bouy.objects.all()
        serializer = BouySerializer(bouys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BouySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Sensors(APIView):

    def get(self, request, format=None):
        sensors = models.Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Bouy(APIView):
    def get(self, request, pk, format=None):
        bouy = models.Bouy.objects.get(pk=pk)
        serializer = BouySerializer(bouy, many=True)
        return Response(serializer.data)

class Sensor(APIView):
    def get(self, request, pk, format=None):
        sensor = models.Sensor.objects.get(pk=pk)
        serializer = BouySerializer(sensor, many=True)
        return Response(serializer.data)