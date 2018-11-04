# Source: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Source2: https://stackoverflow.com/questions/16143842/raspberry-pi-gpio-events-in-python

import RPi.GPIO as GPIO
import time

TOUCH_PIN = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
display_num = 1

def touch_callback(channel):
	global display_num
	if display_num == 1:
		if GPIO.input(TOUCH_PIN) == 1:
			display_num = 0
		else:
			display_num = 1
	else:
		if GPIO.input(TOUCH_PIN) == 1:
			display_num = 1
		else:
			display_num = 0

GPIO.add_event_detect(TOUCH_PIN, GPIO.RISING, callback=touch_callback)

while True:
	time.sleep(5)
	print(display_num)

'''
while True:
	if GPIO.input(TOUCH_PIN) == 1:
		print('HEY')
	else:
		pass
	#print(GPIO.input(TOUCH_PIN))
	time.sleep(1)
'''
