# Source: www.instructables.com/id/Sound-Sensor-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

TOUCH_PIN = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
display_num = 1

def touch_callback(channel):
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
