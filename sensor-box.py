#!/usr/bin/env python3

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

import os
from os.path import exists
import time
import datetime
import sys
import socket

import qwiic_ccs811
import qwiic_bme280
import smbus

import constants
import logger

DEBUG=False
HASPM25=False
baseline = constants.maxBaseline

def checkBaseline(baseValues):
    if (baseValues[0]
        == baseValues[1]
        == baseValues[2]
        == baseValues[3]
        == baseValues[4]
        == baseValues[5]):
        logger.logEvent("all baselines equal, returning True")
        return True

    min = 65530 # initialization level
    max = 0
    for i in baseValues:
        logger.logEvent ("baseline " + str(i))
        if (i == 0):
            logger.logEvent ("0, returning False")
            return False
        if (i <= min):
            min = i
            logger.logEvent ("new min " + str(min))
        if (i >= max):
            max = i
            logger.logEvent ("new max " + str(max))

    logger.logEvent("min max " + str(min) + " " + str(max))
    noise = (abs (max - min))
    if (noise < 2):
        if (DEBUG):
            logger.logEvent("noise " + str(noise) + " baselines " + str(baseValues))
        return True

    return False

def main():
    constants.hostname = socket.gethostname()
    if ((len(constants.hostname) < 1)
        or (constants.hostname == "undefined")):
        print("could not determine hostname")
        sys.exit()

    os.chdir("/home/pi/Projects/sensor-box")
    logger.logEvent("sensor-box.py started at " + str(datetime.datetime.now()))
    # using CCS811 mode 1 for internal measurement every second
    ccs811Sensor = qwiic_ccs811.QwiicCcs811()
    bme280Sensor = qwiic_bme280.QwiicBme280()
    if (HASPM25):
        pm25Sensor = smbus.SMBus(1)
    pm1count = -1
    pm10count = -1
    pm25count = -1
    if (ccs811Sensor.connected == False) or (bme280Sensor.connected == False):
        logger.logEvent("failed to connect to sensors")
        sys.exit(-1)

    ccs811Sensor.begin()
    bme280Sensor.begin()

    yesterday = 0
    today = 1
    baseValues = [ 0, 0, 0, 0, 0, 0]
    baseValueSet = False
    baseValue = 0
    baseIndex = 0

    config = constants.hostname + ".conf"
    if (exists(config)):
        with open(config) as c:
            baseValue = int(c.read())
            ccs811Sensor.set_baseline(baseValue)
            baseValueSet = True
            if (DEBUG):
                print("read baseline from " + config)

    while True:
        today = time.localtime().tm_mday
        if (yesterday != today):
            if (DEBUG):
                print("yesterday", yesterday, "not equal to today",today)
                logger.logEvent("yesterday "  + str(yesterday) + " not equal to today " + str(today))
            uptime = os.popen('uptime -s').read() [:-1]
            logger.logSensorHeader("#boot time " + uptime)
            logger.logSensorHeader("time,temp,humid,CO2,tVOC,PM1.0,PM2.5,PM10.0")
            logger.logEventHeader("#boot time " + uptime)
            logger.logEventHeader("#description of event")

            baseline = ccs811Sensor.get_baseline()
            logger.logEvent("#baseline at day rollover " + str(baseline))
            yesterday = today
            if (baseline != baseValue) and (baseValueSet == True):
                if (DEBUG):
                    logger.logEvent("#baseline " + str(baseline) + " does not match baseValue " + str(baseValue) + ", resetting")
                ccs811Sensor.set_baseline(baseValue)
                
            
        if (baseValueSet == False):
            interval = 10
            if ((time.localtime().tm_min % interval) == 0):
                baseline = ccs811Sensor.get_baseline()
                if (baseline >= constants.maxBaseline):
                    if (DEBUG):
                        logger.logEvent("baseline too high, using 0: " + str(baseline))
                    baseline = 0
                if (DEBUG):
                    logger.logEvent("#baseline " + str(interval) + " min read " + str(baseline))
                baseValues[baseIndex] = baseline
                baseIndex +=1
                logger.logEvent("#basevalues " + str(baseValues))
                if (baseIndex == 6):
                    baseIndex = 0
                if (checkBaseline(baseValues)):
                    logger.logEvent("#baseline set to " + str(baseline))
                    baseValue = baseline
                    ccs811Sensor.set_baseline(baseValue)
                    with open(config, 'w') as c:
                        c.write(str(baseValue))
                    baseValueSet = True
        else:
            interval = 10
            if ((time.localtime().tm_min % interval) == 0):
                baseline = ccs811Sensor.get_baseline()
                if (DEBUG):
                    logger.logEvent("#baseline " + str(interval) + " min read " + str(baseline))
                if (baseline != baseValue) and (baseValueSet == True):
                    if (DEBUG):
                        logger.logEvent("#baseline " + str(baseline) + " does not match baseValue " + str(baseValue) + ", resetting")
                    ccs811Sensor.set_baseline(baseValue)
        humidity = bme280Sensor.humidity
        
        if (HASPM25):
            pm25Data = pm25Sensor.read_i2c_block_data(0x12, 0x00, 32)
            pm1count = (pm25Data[4]<<8) + pm25Data[5]
            pm10count = (pm25Data[8]<<8) + pm25Data[9]
            pm25count = (pm25Data[6]<<8) + pm25Data[7]

        tempCelsius = bme280Sensor.temperature_celsius
        ccs811Sensor.set_environmental_data(humidity, tempCelsius)

        #TODO my stretto reads 4C lower than the reported temperature
        #tempCelsius -= 4

        if ccs811Sensor.data_available():
            ccs811Sensor.read_algorithm_results()
            if (ccs811Sensor.CO2 > 2**14):
                logString = '#error CO2 {:.2f}'.format(ccs811Sensor.CO2)
                logger.logEvent(logString)
            elif (ccs811Sensor.TVOC > 2**14):
                logString = '#error tVOC {:.2f}'.format(ccs811Sensor.TVOC)
                logger.logEvent(logString)
            else:
                logString = '{:.2f},{:.2f},{:d},{:d},{:d},{:d},{:d}'.format(
                    tempCelsius, humidity, 
                    ccs811Sensor.CO2,
                    ccs811Sensor.TVOC,
                    pm1count, pm25count, pm10count)
                logger.logSensor(logString)
                if DEBUG:
                    print(logString)
        time.sleep(60)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\keyboard interrupt")
        sys.exit(0)


