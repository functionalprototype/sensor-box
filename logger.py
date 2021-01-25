import constants

import sys
from datetime import datetime

def logEventFile(category, now, s):
    dateNow = datetime.fromtimestamp(now)
    fileDate = dateNow.strftime("%Y-%m-%d")
    if (category == "sensor"):
        fileName = constants.sensorFilePrefix + fileDate + ".log"
    elif (category == "event"):
        fileName = constants.eventFilePrefix + fileDate + ".log"
    else:
        print("unrecognized category %s" % category)
        sys.exit(-1)
    logEntry = f"{int(now)},{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

def logEventFileHeader(category, now, s):
    dateNow = datetime.fromtimestamp(now)
    fileDate = dateNow.strftime("%Y-%m-%d")
    if (category == "sensor"):
        fileName = constants.sensorFilePrefix + fileDate + ".log"
    elif (category == "event"):
        fileName = constants.eventFilePrefix + fileDate + ".log"
    else:
        print("unrecognized category %s" % category)
        sys.exit(-1)
    logEntry = f"{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

