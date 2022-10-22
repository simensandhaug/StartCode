import re
import pandas as pd
from datetime import datetime, timedelta

from parsers.sensorparser import SensorParser

class PressureSensorParser(SensorParser):
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
        startTimes = [self.parseDate(s) for s in data[0::2]]
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
                parsedMeasurement = {"time_stamp": currentTime}
                if measurement[0] == "b''":
                    parsedMeasurement["depth"] = None
                    parsedMeasurement["pressure"] = None
                    parsedMeasurement["temperature"] = None
                else:
                    splitISDP = measurement[0].split(",")
                    parsedMeasurement["depth"] = float(splitISDP[1])
                    parsedMeasurement["pressure"] = float(splitISDP[3])
                    parsedMeasurement["temperature"] = float(splitISDP[5])
                if measurement[1] == "b''":
                    parsedMeasurement["heading"] = None
                    parsedMeasurement["pitch"] = None
                    parsedMeasurement["roll"] = None
                else:
                    splitISHPR = measurement[1].split(",")
                    parsedMeasurement["heading"] = float(splitISHPR[1])
                    parsedMeasurement["pitch"] = float(splitISHPR[2])
                    parsedMeasurement["roll"] = float(splitISHPR[3])
                parsedData.append(parsedMeasurement)
        return parsedData


