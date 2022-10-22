from unittest.util import _MAX_LENGTH
from django.db import models

class Buoy(models.Model):
    b_id = models.IntegerField(primary_key=True)


class Sensor(models.Model):
    s_id = models.IntegerField(primary_key=True)
    s_type = models.CharField(max_length=40)
    buoy = models.ForeignKey(Buoy, to_field="b_id", related_name="sensors", on_delete=models.CASCADE)
    
class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    
class BuoyMeasurement(Measurement):
    altitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
class LightMeasurement(Measurement):
    light_level = models.FloatField()
    
class EchoLocationMeasurement(Measurement):
    data = models.IntegerField() #????
    
    
    