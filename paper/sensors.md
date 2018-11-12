Sensors
=======

This section is to be completed by the students of the class.

Task is to develop an object oriented class for one of the sensors. An
example for such a class can be found at:

-   <https://github.com/cloudmesh/cloudmesh.pi/blob/master/cloudmesh/pi/led.py>


Temperature and Humidity Sensor Module
--------------------------------------

The temperature and humidity sensor used in this example is the DHT11 sensor which can be purchased as a part of the [Kookye Smart Home Sensor kit](https://www.amazon.com/gp/product/B01J9GD3DG/ref=oh_aui_detailpage_o03_s01?ie=UTF8&psc=1) or the [Elegoo Uno Kit.](https://www.amazon.com/ELEGOO-Project-Starter-Tutorial-Arduino/dp/B01D8KOZF4/ref=sr_1_6?s=electronics&ie=UTF8&qid=1542065611&sr=1-6&keywords=dht11+temperature+and+humidity+module) 

![DHT11 Setup](images/DHT11_setup.png){#fig:dht11_setup}


[Temperature and Humidity Sensor Class](https://github.com/cloudmesh-community/fa18-523-84/tree/master/paper/code)


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
