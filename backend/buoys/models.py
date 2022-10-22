from django.db import models


class Buoy(models.Model):
    b_id = models.IntegerField(primary_key=True)


class Sensor(models.Model):
    s_id = models.IntegerField(primary_key=True)
    s_type = models.CharField(max_length=40)
    buoy = models.ForeignKey(Buoy, to_field="b_id", related_name="sensors", on_delete=models.CASCADE)
    
class BuoyMeasurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="buoy_measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    altitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
class LightMeasurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="light_measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    light_level = models.FloatField()
    
class EchoLocationMeasurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="echo_measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    data = models.IntegerField() #???
    
    
    