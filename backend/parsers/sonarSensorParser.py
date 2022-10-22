
import re
import pandas as pd
from datetime import datetime, timedelta

from parsers.sensorparser import SensorParser

class SonarSensorParser(SensorParser):
    def __init__(self):
        super().__init__()
    
    def parseData(self, data, metadata):

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
        filetext = "".join(data)
        fileTextDividedByStartTimes = re.findall(r"(sampling.*\n.*(?:(?=sampling)|$))", filetext)
        startTimeDataSets = [s.split("\n") for s in fileTextDividedByStartTimes]
        startTimeDataSetsWithParsedTime = [(self.parseDate(s[0]), s[1]) for s in startTimeDataSets]
        parsedSets = [(s[0], re.findall(r"Distance: (\d+|None)\sConfidence: (?:(\d+)%|None)",s[1])) for s in startTimeDataSetsWithParsedTime]
        parsedData = []
        for startTime, measurements in parsedSets:
            for i, measurement in enumerate(measurements):
                currentTime = startTime + i * timedelta(seconds=1/float(metadata["frequency"]))
                parsedMeasurement = {"time_stamp": currentTime}
                if measurement[0] in ("None", ""):
                    parsedMeasurement["distance"] = None
                else:
                    parsedMeasurement["distance"] = float(measurement[0])
                if measurement[1] in ("None", ""):
                    parsedMeasurement["confidence"] = None
                else:
                    parsedMeasurement["confidence"] = float(measurement[1])
                parsedData.append(parsedMeasurement)

        return parsedData