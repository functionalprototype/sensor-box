import constants

import sys
from datetime import datetime

def logEventFile(now, s):
    dateNow = datetime.fromtimestamp(now)
    fileDate = dateNow.strftime("%Y-%m-%d")
    fileName = constants.eventFilePrefix + fileDate + ".log"
    logEntry = f"{int(now)}:{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

