# Code modified from source: https://tutorials-raspberrypi.com/raspberry-pi-control-relay-switch-via-gpio/

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

RELAY_GPIO_1 = 16
RELAY_GPIO_2 = 18

GPIO.setup(RELAY_GPIO_1, GPIO.OUT)
GPIO.setup(RELAY_GPIO_2, GPIO.OUT)



while True:
	print('Heat On')
	GPIO.output(RELAY_GPIO_1, GPIO.LOW)
	time.sleep(3)

	print('Heat Off')
	GPIO.output(RELAY_GPIO_1, GPIO.HIGH)
	time.sleep(3)

	print('AC On')
	GPIO.output(RELAY_GPIO_2, GPIO.LOW)
	time.sleep(3)

	print('AC Off')
	GPIO.output(RELAY_GPIO_2, GPIO.HIGH)
	time.sleep(3)


