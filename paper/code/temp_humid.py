# example of a class used for DHT11 temp and humididy sensor.
# Sources: 
#	http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/
#	https://github.com/adafruit/Adafruit_Python_DHT
# Adafruit_DHT is a dependency of this class.  The code to download Adafruit_DHT can be found at the link below:
#  https://github.com/cloudmesh-community/fa18-523-84/blob/master/project-code/thermostat_setup.sh

import sys
import time
import Adafruit_DHT

class READ_DHT11(object):

	def __init__(self, pin=4):  # pin uses GPIO numbers and defaults to GPIO 4 
		self.pin = pin
		self.sensor = Adafruit_DHT.DHT11

	def return_data(self, temp_measure='celcius'):
		humid, temp = Adafruit_DHT.read_retry(self.sensor, self.pin)
		if humid is not None and temp is not None and temp_measure == 'celcius':
			return humid, temp
		elif humid is not None and temp is not None and temp_measure == 'farenhiet':
			temp = temp * 9.0 / 5.0 + 32.0
			return humid, temp
		else:
			print('Error: no reading detected')
			return


# loop to read temp and humidity

while True:
	humid, temp = READ_DHT11(pin=4).return_data(temp_measure='farenhiet')
	print('Temp: '+str(temp)+u'\u00b0'+'F  Humidity:'+str(humid)+'%')
	time.sleep(1)
