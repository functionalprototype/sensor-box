#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_ccs811_ex7.py
#
# Simple Example for the Qwiic CCS811 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 3
#

from __future__ import print_function
import qwiic_ccs811
import qwiic_bme280
import time
import sys

# Define some error messages
_deviceErrors = { \
	1 << 5 : "HeaterSupply",  \
    1 << 4 : "HeaterFault", \
    1 << 3 : "MaxResistance", \
    1 << 2 : "MeasModeInvalid",  \
    1 << 1 : "ReadRegInvalid", \
    1 << 0 : "MsgInvalid" \
}

def runExample():

	#print("\nSparkFun CCS811 Sensor Example 3 - NTC data to CCS811 for compensation. \n")
	print("#BME280 + CCS811 example")
	ccs811Sensor = qwiic_ccs811.QwiicCcs811()
	bme280Sensor = qwiic_bme280.QwiicBme280()

	if ccs811Sensor.connected == False:
		print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	if bme280Sensor.connected == False:
		print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	ccs811Sensor.begin()
	bme280Sensor.begin()

	print("time,temp,humid,co2,tvoc");
	while True:

		humidityVariable = bme280Sensor.humidity
		temperatureVariable = bme280Sensor.temperature_celsius

		#print("  Humidity:    %.2f percent relative" % humidityVariable)
		#print("  Temperature: %.2f degrees C" % temperatureVariable)

		ccs811Sensor.set_environmental_data(humidityVariable, temperatureVariable)
		if ccs811Sensor.data_available():

			ccs811Sensor.read_algorithm_results()

			#print("  CO2:\t%.3f ppm" % ccs811Sensor.CO2)
			#print("  tVOC:\t%.3f ppb\n" % ccs811Sensor.TVOC)	
			#print(time.asctime(),",",temperatureVariable, ",", humidityVariable, ",", ccs811Sensor.CO2,",",ccs811Sensor.TVOC)
			print("%s,%.2f,%.2f,%d,%d" % 
			(time.asctime(), temperatureVariable,
			humidityVariable, ccs811Sensor.CO2,ccs811Sensor.TVOC))

		elif ccs811Sensor.check_status_error():

			error = ccs811Sensor.get_error_register();
			if error == 0xFF:   
				# communication error
				print("Failed to get Error ID register from sensor")
			else:
				strErr = "Unknown Error"
				for code in _deviceErrors.keys():
					if error & code:
						strErr = _deviceErrors[code]
						break
				print("Device Error: %s" % strErr)

		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)


