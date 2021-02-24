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

import constants
import logger

import qwiic_ccs811
import qwiic_bme280
import time
import sys

import smbus

DEBUG=False
HASPM25=True

today = 1

def main():
    # using CCS811 mode 1 for internal measurement every second
    ccs811Sensor = qwiic_ccs811.QwiicCcs811()
    bme280Sensor = qwiic_bme280.QwiicBme280()
    pm25Sensor = smbus.SMBus(1)
    pm1count = -1
    pm10count = -1
    pm25count = -1
    if (ccs811Sensor.connected == False) or (bme280Sensor.connected == False):
        print("failed to connect to sensors")
        sys.exit(-1)

    ccs811Sensor.begin()
    bme280Sensor.begin()

    yesterday = 0
    while True:
        today = time.localtime().tm_mday
        if (yesterday != today):
            print("yesterday", yesterday, "not equal to today",today)
            logger.logSensorHeader("time,temp,humid,CO2,tVOC,PM1.0,PM2.5,PM10.0")
            logger.logEventHeader("description of event")
            yesterday = today

        humidity = bme280Sensor.humidity
        #my stretto reads 4C lower than the reported temperature
        tempCelsius = bme280Sensor.temperature_celsius - 4
        
        if (HASPM25):
            pm25Data = pm25Sensor.read_i2c_block_data(0x12, 0x00, 32)
            pm1count = (pm25Data[4]<<8) + pm25Data[5]
            pm10count = (pm25Data[8]<<8) + pm25Data[9]
            pm25count = (pm25Data[6]<<8) + pm25Data[7]

        ccs811Sensor.set_environmental_data(humidity, tempCelsius)

        if ccs811Sensor.data_available():
            ccs811Sensor.read_algorithm_results()
            if (ccs811Sensor.CO2 > 2**15):
                logString = '#error CO2 {:.2f}'.format(ccs811Sensor.CO2)
                logger.logEvent(logString)
                print("CO2 sensor out of range", ccs811Sensor.CO2)
            elif (ccs811Sensor.TVOC > 2**15):
                print("tVOC sensor out of range", ccs811Sensor.TVOC)
                logString = '#error tVOC {:.2f}'.format(ccs811Sensor.TVOC)
                logger.logEvent(logString)
                print("tVOC sensor out of range", ccs811Sensor.TVOC)
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


