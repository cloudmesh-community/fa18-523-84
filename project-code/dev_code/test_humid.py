#Source: http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4

while True:
	humid, temp = Adafruit_DHT.read_retry(sensor, pin)
	if humid is not None and temp is not None:
		print('Temp: '+str(temp)+'C  Humidity:'+str(humid)+'%')
	else:
		print('Error')
