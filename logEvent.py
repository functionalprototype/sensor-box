#!/usr/bin/env python3

#local
import logger
import constants

import sys
import time

def logEvent(s):
    now = time.time()
    logger.logEventFile("event", now, s)

def logSensor(s):
    now = time.time()
    logger.logEventFile("sensor",now, s)

