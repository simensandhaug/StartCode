import re
import pandas as pd
from datetime import datetime, timedelta

def parseDate(date: str) -> datetime:
    return datetime.strptime(date.strip(), '%a, %d %b %Y %H:%M:%S %z')

with open("trykksensor.txt", "r") as file:
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
    headers = [s.strip() for s in file.readline().split(",")]
    values = [s.strip() for s in file.readline().split(",")]
    metadata = {headers[i]: values[i] for i in range(len(headers))}
    data = file.readlines();
    startTimes = [parseDate(re.search("(?<=:).*", s).group()) for s in data[0::2]]
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
    df = pd.DataFrame(parsedData, columns=["time", "depth in meters", "absolute pressure in bar", "temperature in degrees Celsius", "heading in degrees", "pitch in degrees", "roll in degrees"])
    df.to_csv("trykksensor.csv", index=False)