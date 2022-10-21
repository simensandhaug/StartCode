from django.contrib import admin
from .models import *

admin.site.register(Buoy)
admin.site.register(Sensor)
admin.site.register(Measurement)
admin.site.register(BuoyMeasurement)
admin.site.register(LightMeasurement)
admin.site.register(EchoLocationMeasurement)