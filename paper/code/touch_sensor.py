# Source: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Source2: https://stackoverflow.com/questions/16143842/raspberry-pi-gpio-events-in-python

import RPi.GPIO as GPIO
import time


class touch_sensor(object):
	"""docstring for touch_sensor"""
	def __init__(self, pin=7, pin_setup='BOARD'):
		self.pin = pin
		if pin_setup == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else:
			GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.IN)		
		GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.touch_callback)
		display_num = 1
		global display_num
		
	def touch_callback(self, channel):
		if display_num == 1:
			if GPIO.input(self.pin) == 1:
				display_num = 0
			else:
				display_num = 1
		else:
			if GPIO.input(self.pin) == 1:
				display_num = 1
			else:
				display_num = 0
		return display_num

while True:
	time.sleep(1)
	print(touch_sensor())
