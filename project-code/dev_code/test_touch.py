# Source: www.instructables.com/id/Sound-Sensor-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

touch_pin = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	if GPIO.input(touch_pin) == 1:
		print('HEY')
	else:
		pass
	#print(GPIO.input(touch_pin))
	time.sleep(1)
