from django.contrib import admin
from .models import *

admin.site.register(Bouy)
admin.site.register(Sensor)
admin.site.register(Measurement)
admin.site.register(BouyMeasurement)
admin.site.register(LightMeasurement)
admin.site.register(EchoLocationMeasurement)