from datetime import timedelta
import ast

from parsers.sensorparser import SensorParser

class GyroscopeSensorParser(SensorParser):
    def __init__(self):
        super().__init__()

    def eval_line(self, line):
        isdpt, depth, _, pressure, _ = line[0].split(",")
        return (isdpt, float(depth), float(pressure))
    
    def parseData(self, data, metadata):
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
        total_lines = len(data)
        i = 0
        measurementPairs = []
        while i < total_lines-1:
            sample_start_parsed = self.parseDate(data[i])
            line = ast.literal_eval(data[i+1])
            line_len = len(line)
            # float_measurements = data_lines[i:i+line_len]
            i += line_len + 2
            for j in range(line_len):
                line[j] = self.eval_line(line[j])
            if(line_len > 0):
                measurementPairs.append([sample_start_parsed, line])

        # Convert to a list of dicts
        parsedData = []
        for startTime, measurements in measurementPairs:
            for i, measurement in enumerate(measurements):
                currentTime = startTime + i * timedelta(seconds=1/float(metadata["frequency"]))
                parsedMeasurement = {"time_stamp": currentTime}
                _, depth, pressure = list(measurement)
                parsedMeasurement["depth"] = depth
                parsedMeasurement["pressure"] = pressure
                parsedData.append(parsedMeasurement)
        return parsedData
