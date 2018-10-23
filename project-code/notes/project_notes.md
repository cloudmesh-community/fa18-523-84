Notes for the class project
===========================

**Project: Attempt to build a smart theromstat**

  * Use raspberry pi to collect data and manage temperature.
  * Send data to cloud to store in a database and to run analytics
  * Combine weather forecast data to help predict what the temperature should be set at
  * Look at how expenses have improved as a result. Graph savings and energy usage.
  * Create an interface to look at this data.

**Project Status**

Raspberry Pi used for thermostat

 * [x] Order sensors for raspberry pi thermostat (temperature, motion, etc)
 * [x] Set up raspberry pi
 * [x] Set up temperature sensor

Python code

 * [x] Python code to get weather forecast
 * [ ] Set up cassandra data base to store data from weather and sensors
 
Raspberry Pi cluster
 
 * [ ] Set up OS on each pi in the cluster
 * [ ] Code to configure the nodes?

**Resources**

*Look into particle for IoT: https://www.particle.io/*

 * Video on how to use Docker: https://www.youtube.com/watch?v=wCTTHhehJbU

 * Thermostats: https://dzone.com/articles/how-to-build-your-own-arduino-thermostat
 * How to set up a raspberry pi temperature sensor: http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
 * Python weather API: https://pypi.org/project/weather-api/
 * Python geolocation API: https://geocoder.readthedocs.io/
 * Keep process alive after closing ssh session: https://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session
 * Node-RED: https://nodered.org/
 * Node-RED MQTT Setup: https://cookbook.nodered.org/basic/
 
