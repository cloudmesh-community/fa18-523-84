Sensors
=======

This section is to be completed by the students of the class.

Task is to develop an object oriented class for one of the sensors. An
example for such a class can be found at:

-   <https://github.com/cloudmesh/cloudmesh.pi/blob/master/cloudmesh/pi/led.py>


Temperature and Humidity Sensor Module
--------------------------------------

```
# Demonstrate class used for DHT11 temp and humididy sensor.
# Code modified from source: http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/
# Adafruit_DHT is a dependency of this class

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
        
```


Compass
-------

TODO: which compass sensor

The default pins are defined in variants/nodemcu/pins_arduino.h as GPIO

    SDA=4 
    SCL=5
    D1=5 
    D2=4.

You can also choose the pins yourself using the I2C constructor
Wire.begin(int sda, int scl);
