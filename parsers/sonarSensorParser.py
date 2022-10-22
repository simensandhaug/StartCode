
import re
import pandas as pd
from datetime import datetime, timedelta

from sensorparser import SensorParser

class SonarSensorParser(SensorParser):
    def __init__(self):
        super().__init__()
    
    def parseData(self, file, metadata):

        # Convert lines to a list like this:
        '''
        [
            (startTime, [
                (ISDPT, ISHPR),
                (ISDPT, ISHPR),
                ...
            ]),
            (startTime, [
                (ISDPT, ISHPR),
                (ISDPT, ISHPR),
                ...
            ]),
            ...
        ]
        '''
        filetext = file.read()
        fileTextDividedByStartTimes = re.findall(r"(sampling.*\n.*(?:(?=sampling)|$))", filetext)
        startTimeDataSets = [s.split("\n") for s in fileTextDividedByStartTimes]
        startTimeDataSetsWithParsedTime = [(self.parseDate(s[0]), s[1]) for s in startTimeDataSets]
        parsedSets = [(s[0], re.findall(r"Distance: (\d+|None)\sConfidence: (?:(\d+)%|None)",s[1])) for s in startTimeDataSetsWithParsedTime]
        print("Hello")
        parsedData = []
        for startTime, measurements in parsedSets:
            for i, measurement in enumerate(measurements):
                currentTime = startTime + i * timedelta(seconds=1/float(metadata["frequency"]))
                parsedMeasurement = []
                if measurement[0] in ("None", ""):
                    parsedMeasurement = [currentTime, None]
                else:
                    parsedMeasurement = [currentTime , float(measurement[0])]
                if measurement[1] in ("None", ""):
                    parsedMeasurement += [None]
                else:
                    parsedMeasurement += [float(measurement[1]) ]
                parsedData.append(parsedMeasurement)
        return pd.DataFrame(parsedData, columns=["time", "distance", "confidence"])