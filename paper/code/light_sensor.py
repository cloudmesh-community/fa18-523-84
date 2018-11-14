# Python3
# Source: www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

import RPi.GPIO as GPIO
import time

class READ_LIGHT_SENSOR(object):
	"""Pin numbers for READ_LIGHT_SENSOR are based on BOARD numbers by default"""
	def __init__(self, pin=7, pin_setup='BOARD'):
		self.pin = pin
		if pin_setup == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else:
			GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.IN)
			
	def return_data(self, pin):
		return GPIO.input(self.pin)

while True:
	print(READ_LIGHT_SENSOR(pin=11).return_data())
	time.sleep(1)
