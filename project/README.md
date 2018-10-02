Raspberry Pi IOT - Smart Thermostat & Cloud Data Storage
========================================================

**Overview:**

This project aims to explore how the internet of things works by building a smart thermostat.  The thermostat will collect data about the current indoor environment as well as the outdoor environment.  This data will be sent to a cassendra NoSQl cluster that is run in the cloud.  This data will be accessed by the thermostat as well as an application that can be accessed to view the data.

**Hardware Needed:**

Thermostat

  * DS18B20 Temperature Sensor
  * Small breadboard & connector wires
  * 4.7k ohm resistor
  * Raspbeery Pi

Cloud Cluster

  * 5 Raspberry Pi
  * Network switch & cables
  
**Install & Setup:**

Shell code to set up python to run the program.

```shell
#!/bin/bash

sudo apt-get python3-pandas
pip3 install pyowm
pip3 install geocoder
echo "All python dependencies have been successfully installed."

```
