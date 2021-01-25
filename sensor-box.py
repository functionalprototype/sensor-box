#!/usr/bin/env python3

import constants
import logEvent

import qwiic_ccs811
import qwiic_bme280
import time
import sys

DEBUG=False

def main():
	ccs811Sensor = qwiic_ccs811.QwiicCcs811()
	bme280Sensor = qwiic_bme280.QwiicBme280()

	if (ccs811Sensor.connected == False) or (bme280Sensor.connected == False):
		print("failed to connect to sensors")
		sys.exit(-1)
        
	ccs811Sensor.begin()
	bme280Sensor.begin()

	logEvent.logSensorHeader("#time,temp,humid,co2,tvoc")
	logEvent.logEventHeader("#description of event")

	while True:

		humidity = bme280Sensor.humidity
		tempCelsius = bme280Sensor.temperature_celsius
		ccs811Sensor.set_environmental_data(humidity, tempCelsius)

		if ccs811Sensor.data_available():
			ccs811Sensor.read_algorithm_results()
			if (ccs811Sensor.CO2 > 2**15):
				logString = '#error CO2 {:.2f}'.format(ccs811Sensor.CO2)
				logEvent.logSensor(logString)
				print("CO2 sensor out of range", ccs811Sensor.CO2)
				
			elif (ccs811Sensor.TVOC > 2**15):
				print("tVOC sensor out of range",
					 ccs811Sensor.TVOC)
				logString = '#error tVOC {:.2f}'.format(ccs811Sensor.TVOC)
				logEvent.logSensor(logString)
				print("tVOC sensor out of range", ccs811Sensor.TVOC)
			else:
				logString = '{:.2f},{:.2f},{:d},{:d}'.format(
				tempCelsius, humidity, 
				ccs811Sensor.CO2,ccs811Sensor.TVOC)
				logEvent.logSensor(logString)
				if DEBUG:
					print(logString)

		time.sleep(1)


if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\keyboard interrupt")
		sys.exit(0)


