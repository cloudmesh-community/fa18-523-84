#!/bin/bash

#install python packages
sudo apt-get install python3-pip

# code for humidity sensor on git hub
# Source: https://stackoverflow.com/questions/28913592/python-gpio-code-for-dht-11-temperature-sensor-fails-in-pi-2
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo python setup.py install

sudo apt-get python3-pandas
pip3 install pyowm
pip3 install geocoder
pip3 install RPi
pip3 install RPLCD
sudo easy_install3 timezonefinder
sudo easy_install3 cassandra-driver
echo "All python dependencies have been successfully installed."

#install cassandra
#mkdir ~/cassandra
#cd cassandra
# https://academy.datastax.com/all-downloads?field_download_driver_category_tid=910
#wget ""





