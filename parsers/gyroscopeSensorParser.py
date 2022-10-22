import pandas as pd
from datetime import timedelta
import ast

from sensorparser import SensorParser

class GyroscopeSensorParser(SensorParser):
    def __init__(self):
        super().__init__()

    def eval_line(self, line):
        isdpt, depth, _, pressure, _ = line[0].split(",")
        return (isdpt, float(depth), float(pressure))
    
    def parse_start_date(self, sample_start):
        return sample_start.strip()[21:]
    
    def parseData(self, file, metadata):
        # Convert lines to a list like this:
        '''
        [
            (startTime, [
                (ISDPT),
                (ISDPT),
                ...
            ]),
            (startTime, [
                (ISDPT),
                (ISDPT),
                ...
            ]),
            ...
        ]
        '''
        data = file.readlines();
        total_lines = len(data)
        i = 0
        measurementPairs = []
        while i < total_lines-1:
            sample_start = self.parse_start_date(data[i])
            sample_start_parsed = self.parseDate(sample_start)
            line = ast.literal_eval(data[i+1])
            line_len = len(line)
            # float_measurements = data_lines[i:i+line_len]
            i += line_len + 2
            for j in range(line_len):
                line[j] = self.eval_line(line[j])
            if(line_len > 0):
                measurementPairs.append([sample_start_parsed, line])

        # Convert to a pandas dataframe
        parsedData = []
        for startTime, measurements in measurementPairs:
            for i, measurement in enumerate(measurements):
                currentTime = startTime + i * timedelta(seconds=1/float(metadata["frequency"]))
                #print(currentTime)
                splitISDP = [currentTime] + list(measurement[1:])
                parsedData.append(splitISDP)
        return pd.DataFrame(parsedData, columns=["time", "depth in meters", "absolute pressure in bar"])