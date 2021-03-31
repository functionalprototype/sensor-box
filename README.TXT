sensor-box

Domestic/residential box to host Qwiic and other sensors, collect
data, generate reports, generate warnings.

Initial goals are for collecting information on kitchen air quality
while cooking, baking, or doing an oven self-clean.

This is not a replacement for fire alarms, CO2 detectors, or other
safety devices.


pip3 dependencies:

sudo pip3 install sparkfun-qwiic
sudo pip3 install adafruit-circuitpython-pm25


setting up systemd:

sudo cp -i sensorbox.service /etc/systemd/system/sensorbox.service 
sudo systemctl daemon-reload
sudo systemctl enable sensorbox
sudo systemctl start sensorbox
