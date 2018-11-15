# Code modified from source: https://tutorials-raspberrypi.com/raspberry-pi-control-relay-switch-via-gpio/
# Actual pins in example: relay 1 = 16; relay 2 = 18

import RPi.GPIO as GPIO
import time


class relay_switch(object):
	"""docstring for relay_switch
	currently set up for a 2 channel relay
	"""
	def __init__(self, pin=8, pin2='', pin_setup='BOARD'):
		self.pin = pin
		self.pin2 = pin2
		if pin_setup == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else:
			GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin, GPIO.OUT)
		if self.pin2 != '':
			GPIO.setup(self.pin2, GPIO.OUT)
		else:
			pass
		
	def relay_on(self, relay_num=1):
		if relay_num == 1:
			GPIO.output(self.pin, GPIO.LOW)
		elif relay_num == 2:
			GPIO.output(self.pin2, GPIO.LOW)
		else:
			return

	def relay_off(self, relay_num=1):
		if relay_num == 1:
			GPIO.output(self.pin, GPIO.HIGH)
		elif relay_num == 2:
			GPIO.output(self.pin2, GPIO.HIGH)
		else:
			return


while True:
	time.sleep(5)
	counter = 10
	while counter > 0:
		relay_switch(pin=16).relay_on()
		time.sleep(0.5)
		relay_switch(pin=16).relay_off()
		time.sleep(0.5)
