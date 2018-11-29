# Python3
# Source: www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

import RPi.GPIO as GPIO
import time
import sys
import os

class READ_LIGHT_SENSOR(object):
	"""Pin numbers for READ_LIGHT_SENSOR are based on BOARD numbers by default.
	The number 1 will be returned if the light sensor is off and 0 if the sensor is activated.
	"""
	def __init__(self, pin=7, pin_setup='BOARD'):
		self.pin = pin
		if pin_setup == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else:
			GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.IN)
			
	def get(self):
		return GPIO.input(self.pin)


if __name__ == '__main__':
	try:
		light = READ_LIGHT_SENSOR(pin=11)
		while True:
			print(light.get())
			time.sleep(1)
	except KeyboardInterrupt:
		print('\n\n *** Stopping Program ***')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
