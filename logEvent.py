#!/usr/bin/env python3

#local
import logger
import constants

import sys
import time

def logEventHeader(s):
    now = time.time()
    logger.logEventFileHeader("event", now, s)

def logEvent(s):
    now = time.time()
    logger.logEventFile("event", now, s)

def logSensorHeader(s):
    now = time.time()
    logger.logEventFileHeader("sensor", now, s)

def logSensor(s):
    now = time.time()
    logger.logEventFile("sensor", now, s)

