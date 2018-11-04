# Source: www.instructables.com/id/Sound-Sensor-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

sound_pin = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	#if GPIO.input(sound_pin) == False:
	#	print('Sound Detected')
	#else:
	#	pass
	print(GPIO.input(sound_pin))
	time.sleep(2)
