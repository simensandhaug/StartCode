from django.contrib import admin
from .models import *

admin.site.register(Buoy)
admin.site.register(Sensor)
admin.site.register(BuoyMeasurement)
admin.site.register(EchoLocationMeasurement)
