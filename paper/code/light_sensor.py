# Python3
# Source: www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

import RPi.GPIO as GPIO
import time

class READ_LIGHT_SENSOR(object):
	"""Pin numbers for READ_LIGHT_SENSOR are based on BOARD numbers by default"""
	def __init__(self, pin=7, pin_setup='BOARD'):
		GPIO.setmode(GPIO.pin_Setup)
		GPIO.setwarnings(False)
		GPIO.setup(pin,GPIO.IN)
		self.pin = pin
		
	def return_data(self, pin):
		return GPIO.input(self.pin) 

while True:
	print(READ_LIGHT_SENSOR(pin=11))
	time.sleep(1)
