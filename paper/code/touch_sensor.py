# Source: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Source2: https://stackoverflow.com/questions/16143842/raspberry-pi-gpio-events-in-python

import RPi.GPIO as GPIO
import time
import os
import sys

class touch_sensor(object):
	"""docstring for touch_sensor"""
	def __init__(self, callback_action, pin=7, pin_setup='BOARD'):
		self.pin = pin
		if pin_setup == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else:
			GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.IN)
		GPIO.remove_event_detect(self.pin)
		GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback(callback_action=callback_action))
		
	def callback(self, channel, callback_action):
		if GPIO.input(self.pin) == 1:
			callback_action
		else:
			pass
		

# wait for touch sensor activation

if __name__ == '__main__':
	try:
		def touch_print(text):
			print(text)

		touch_sensor(callback_action=touch_print('Hey!'), pin=13)
		while True:
			time.sleep(1)		
	except KeyboardInterrupt:
		print('\n\n *** Stopping Program ***')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
