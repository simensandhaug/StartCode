import re
import pandas as pd
from datetime import datetime, timedelta

from sensorparser import SensorParser

class PressureSensorParser(SensorParser):
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
        data = file.readlines();
        startTimes = [self.parseDate(re.search("(?<=:).*", s).group()) for s in data[0::2]]
        measurementSets = [
            re.findall(r"(?<=\$)[^(\\r\\n)]*(?=\*..\\r\\n)|b''",m)
            for m in data[1::2]]
        pairwiseMeasuremnts = [zip(m[::2], m[1::2])for m in measurementSets]
        measurementSetsDividedInPairs = zip(startTimes, pairwiseMeasuremnts)

        # Convert to a pandas dataframe
        parsedData = []
        for startTime, measurements in measurementSetsDividedInPairs:
            for i, measurement in enumerate(measurements):
                currentTime = startTime + i * timedelta(seconds=1/float(metadata["frequency"]))
                print(currentTime)
                parsedMeasurement = []
                if measurement[0] == "b''":
                    parsedMeasurement = [currentTime, None ,None,None]
                else:
                    splitISDP = measurement[0].split(",")
                    parsedMeasurement = [currentTime] + [float(m) for m in splitISDP[1::2]]
                if measurement[1] == "b''":
                    parsedMeasurement += [None, None, None]
                else:
                    splitISHPR = measurement[1].split(",")
                    parsedMeasurement += [float(m) for m in splitISHPR[1:]]
                parsedData.append(parsedMeasurement)
        return pd.DataFrame(parsedData, columns=["time", "depth in meters", "absolute pressure in bar", "temperature in degrees Celsius", "heading in degrees", "pitch in degrees", "roll in degrees"])


