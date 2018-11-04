# Source: www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi/

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.IN)

while True:
	print(GPIO.input(11))
	time.sleep(2)
