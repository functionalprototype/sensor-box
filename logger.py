import constants

import sys
from datetime import datetime

def logEventFile(category, now, s):
    dateNow = datetime.fromtimestamp(now)
    fileDate = dateNow.strftime("%Y-%m-%d")
    if (category == "sensors"):
        fileName = constants.sensorFilePrefix + fileDate + ".log"
    else if (category == "events"):
        fileName = constants.eventFilePrefix + fileDate + ".log"

    logEntry = f"{int(now)}:{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

