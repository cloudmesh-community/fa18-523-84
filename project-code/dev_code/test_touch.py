# Source: www.instructables.com/id/Sound-Sensor-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

TOUCH_PIN = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def touch_callback(channel):
	print('Hey!')

GPIO.add_event_detect(TOUCH_PIN, GPIO.RISING, callback=touch_callback)

while True:
	time.sleep(1)

'''
while True:
	if GPIO.input(TOUCH_PIN) == 1:
		print('HEY')
	else:
		pass
	#print(GPIO.input(TOUCH_PIN))
	time.sleep(1)
'''
