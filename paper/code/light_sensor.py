# Python3
# Source: www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

import RPi.GPIO as GPIO
import time

class READ_LIGHT_SENSOR(object):
	"""Pin numbers for READ_LIGHT_SENSOR are based on GPIO numbers"""
	def __init__(self, pin=4):
		GPIO.setmode(GPIO.GPIO)
		GPIO.setwarnings(False)
		GPIO.setup(pin,GPIO.IN)
		self.pin = pin
		
	def return_data(self, pin):
		return GPIO.input(self.pin) 

while True:
	print(READ_LIGHT_SENSOR(pin=17))
	time.sleep(1)
