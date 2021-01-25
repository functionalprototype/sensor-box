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
import logEvent

from __future__ import print_function
import qwiic_ccs811
import qwiic_bme280
import time
import sys

def main:

	ccs811Sensor = qwiic_ccs811.QwiicCcs811()
	bme280Sensor = qwiic_bme280.QwiicBme280()

	if (ccs811Sensor.connected == False) or (bme280Sensor.connected == False):
		print("failed to connect to sensors")
        sys.exit(-1)
        
	ccs811Sensor.begin()
	bme280Sensor.begin()

	logEvent.logSensor("#time,temp,humid,co2,tvoc")

	while True:

		humidity = bme280Sensor.humidity
		tempCelsius = bme280Sensor.temperature_celsius
		ccs811Sensor.set_environmental_data(humidity, tempCelsius)

		if ccs811Sensor.data_available():
			ccs811Sensor.read_algorithm_results()
            logString = '{:s},{:.2f},{:.2f},{:d},{:d}'.format(
                time.asctime(), tempCelsius,
                humidity, ccs811Sensor.CO2,ccs811Sensor.TVOC))

		time.sleep(1)


if __name__ == '__main__':
	try:
        main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\keyboard interrupt")
		sys.exit(0)


