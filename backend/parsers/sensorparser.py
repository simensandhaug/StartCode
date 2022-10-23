from abc import ABC, abstractmethod
from datetime import datetime
from io import TextIOWrapper
from buoys.models import Sensor
from buoys.serializers import SensorMetadataSerializer

import pandas as pd
class SensorParser(ABC):
    
    def __init__(self):
        pass

    # Read a file and return a dataframe for metadata and one for data
    def parseFile(self, file) -> tuple[dict, list[dict]]:
        headers = [s.strip() for s in file.readline().decode("utf-8").split(",")]
        values = [s.strip() for s in file.readline().decode("utf-8").split(",")]
        metadata = {headers[i]: values[i] for i in range(len(headers))}
        metadataToSave = {"sensor": metadata["sensor"], "s_last_calibrated": datetime.fromtimestamp(int(metadata["last_calibrated"])), "s_calibration_error": metadata["calibration_error"]}
        serializer = SensorMetadataSerializer(data=metadataToSave)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        frequency = Sensor.objects.get(s_id=metadata["sensor"]).s_sample_frequency
        metadata["frequency"] = frequency
        parsedData =  self.parseData([line.decode("utf-8") for line in file.readlines()],metadata)
        for dataPoint in parsedData:
            dataPoint["sensor"] = int(metadata["sensor"])
        return (metadata, parsedData)
    
    def parseDate(self, date: str) -> datetime:
        return datetime.strptime(date.strip(), 'sampling started at :%a, %d %b %Y %H:%M:%S %z')

    @abstractmethod
    def parseData(self, lines: list[str], metadata)->list[dict]:
        pass