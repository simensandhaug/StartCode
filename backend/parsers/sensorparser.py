from abc import ABC, abstractmethod
from datetime import datetime
from io import TextIOWrapper

import pandas as pd
class SensorParser(ABC):
    
    def __init__(self):
        pass

    # Read a file and return a dataframe for metadata and one for data
    def parseFile(self, file) -> tuple[dict, list[dict]]:
        headers = [s.strip() for s in file.readline().decode("utf-8").split(",")]
        values = [s.strip() for s in file.readline().decode("utf-8").split(",")]
        metadata = {headers[i]: values[i] for i in range(len(headers))}
        parsedData =  self.parseData([line.decode("utf-8") for line in file.readlines()],metadata)
        for dataPoint in parsedData:
            dataPoint["sensor"] = int(metadata["id"])
        return (metadata, parsedData)
    
    def parseDate(self, date: str) -> datetime:
        return datetime.strptime(date.strip(), 'sampling started at :%a, %d %b %Y %H:%M:%S %z')

    @abstractmethod
    def parseData(self, lines: list[str], metadata)->list[dict]:
        pass