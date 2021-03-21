# Copyright (c) 2021 Jet Townsend

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import constants

import sys
import time
import socket

def logEventFile(category, timestamp, s):
    now = time.localtime()
    fileDate = '{:04d}-{:02d}-{:02d}'.format(now.tm_year,now.tm_mon,now.tm_mday)
    hostname = socket.gethostname()
    if (category == "sensor"):
        fileName = hostname + "-" + constants.sensorFilePrefix + fileDate + ".log"
    elif (category == "event"):
        fileName = hostname + "-" + constants.eventFilePrefix + fileDate + ".log"
    else:
        print("unrecognized category %s" % category)
        sys.exit(-1)
    logEntry = f"{timestamp},{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

def logEventFileHeader(category, s):
    now = time.localtime()
    fileDate = '{:04d}-{:02d}-{:02d}'.format(now.tm_year,now.tm_mon,now.tm_mday)
    hostname = socket.gethostname()
    if (category == "sensor"):
        fileName = hostname + "-" + constants.sensorFilePrefix + fileDate + ".log"
    elif (category == "event"):
        fileName = hostname + "-" + constants.eventFilePrefix + fileDate + ".log"
    else:
        print("unrecognized category %s" % category)
        sys.exit(-1)
    logEntry = f"{s}\n"
    with open(fileName, 'a') as f:
        f.write(logEntry)

def logEventHeader(s):
    logEventFileHeader("event", s)

def logEvent(s):
    t = time.localtime()
    logEventFile("event", int(time.mktime(t)), s)

def logSensorHeader(s):
    logEventFileHeader("sensor", s)

def logSensor(s):
    t = time.localtime()
    logEventFile("sensor", int(time.mktime(t)), s)

