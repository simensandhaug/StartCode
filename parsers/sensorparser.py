from abc import ABC, abstractmethod
from datetime import datetime
from io import TextIOWrapper

import pandas as pd
class SensorParser(ABC):
    
    def __init__(self):
        pass

    # Read a file and return a dataframe for metadata and one for data
    def parseFile(self, filename:str) -> tuple[pd.DataFrame, pd.DataFrame]:
        with open(filename, "r") as file:
            headers = [s.strip() for s in file.readline().split(",")]
            values = [s.strip() for s in file.readline().split(",")]
            metadataDict = {headers[i]: values[i] for i in range(len(headers))}
            metadataFrame = pd.DataFrame([values], columns=headers)
            return (metadataFrame, self.parseData(file,metadataDict))
    
    def parseDate(self, date: str) -> datetime:
        return datetime.strptime(date.strip(), '%a, %d %b %Y %H:%M:%S %z')

    @abstractmethod
    def parseData(self, file:TextIOWrapper, metadata)->pd.DataFrame:
        pass