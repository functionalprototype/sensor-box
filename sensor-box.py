#!/usr/bin/env python3

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


