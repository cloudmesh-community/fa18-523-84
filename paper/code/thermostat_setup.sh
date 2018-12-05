#!/bin/bash

#run updates
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

echo "INFO: Updates Complete"

#install git
sudo apt-get install git -y
sudo mkdir git-repos
cd git-repos
git clone https://github.com/cloudmesh-community/fa18-523-84.git

echo "INFO: git setup complete"

#install python packages
sudo apt-get install python3-pip

# code for humidity sensor on git hub
# Source: https://stackoverflow.com/questions/28913592/python-gpio-code-for-dht-11-temperature-sensor-fails-in-pi-2
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo python setup.py install

#other python modules
sudo apt-get python3-pandas
pip3 install pyowm
pip3 install geocoder
pip3 install RPi
pip3 install RPLCD
sudo easy_install3 timezonefinder

#this takes a long time to run and install.  only needed for the connected version
#sudo easy_install3 cassandra-driver 

echo "INFO: All python dependencies have been successfully installed."







