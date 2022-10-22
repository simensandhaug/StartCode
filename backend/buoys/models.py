from django.db import models


class Buoy(models.Model):
    b_id = models.IntegerField(primary_key=True)


class Sensor(models.Model):
    s_id = models.IntegerField(primary_key=True)
    s_type = models.CharField(max_length=40)
    s_sample_frequency = models.FloatField()
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
class PressureMeasurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="pressure_measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    depth = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    heading = models.FloatField(null=True)
    pitch = models.FloatField(null=True)
    roll = models.FloatField(null=True)
    
class EchoLocationMeasurement(models.Model):
    time_stamp = models.DateTimeField()
    distance = models.FloatField(null=True)
    confidence = models.FloatField(null=True)
    sensor = models.ForeignKey(Sensor, related_name="echo_measurements", on_delete=models.CASCADE)
    
    
    