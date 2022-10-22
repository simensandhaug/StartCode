# BadBuoy-solution

Our solution writes metadata and sensor-measurements into the database from a file that is posted via HTTP to the server.

## Install Requirements

```bash
pip install -r requirements.txt
```

## Activate Virtual Environment

```bash
python -m venv venv
venv/bin/activate
```

## Add new sensor-types

### Example

1. In `models.py` add the Measurement model

```python
from django.db import models

class ExampleMeasurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="example_measurements", on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    example_attribute = models.FloatField()
```
2. In `serializers.py` add the MeasurementSerializer, and create a field for it in the SensorSerializer
```python
class ExampleMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleMeasurement
        fields = '__all__'
        
    def create(self, data):
        return ExampleMeasurement.objects.create(**data)
```

```python
class SensorSerializer(serializers.ModelSerializer):
    ...
    example_measurements = ExampleMeasurementSerializer(read_only=True, many=True, source='filtered_example_measurements')
    ...
```


3. In `views.py` add the Measurement view and update, and add the Prefetch in `get_sensors` function
```python 
class ExampleMeasurementList(APIView):
    def get(self, request, format=None):
        example_measurements = ExampleMeasurement.objects.all()
        serializer = ExampleMeasurementSerializer(example_measurements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExampleMeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
```python
def get_sensors(request):
    ...
    return Sensor.objects.prefetch_related(
        Prefetch('example_measurements', queryset=ExampleMeasurement.objects.filter(Q(time_stamp__gte=start) & Q(time_stamp__lte=end)), to_attr='filtered_example_measurements'),
    )
    ...
```

4. In `urls.py` add the new endpoint

```python
urlpatterns = [
    ...
    path('measurements/example/', ExampleMeasurementList.as_view()),
    ...
]
```

> Remember to make migrations and migrate the database afterwards
