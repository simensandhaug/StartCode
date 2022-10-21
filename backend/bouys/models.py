from unittest.util import _MAX_LENGTH
from django.db import models

class Bouy(models.Model):
    b_id = models.IntegerField()
    

class Sensor(models.Model):
    s_id = models.IntegerField()
    s_type = models.CharField(max_length=40)
    bouy = models.ForeignKey(Bouy, on_delete=models.CASCADE)
    
class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    
class BouyMeasurement(Measurement):
    altitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
class LightMeasurement(Measurement):
    light_level = models.FloatField()
    
class EchoLocationMeasurement(Measurement):
    data = models.IntegerField() #????
    
    
    