#!/bin/bash

#update / upgrade
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

echo "INFO: updates complete"

#install nmap for networking
sudo apt-get install nmap
sudo apt-get install apache2
sudo apt-get remove libapache2-mod-python libapache2-mod-wsgi
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi

echo "INFO: tools and dependancies installed"

#install python packages
sudo apt-get install python3-pip
sudo apt-get install python3-pandas
sudo easy_install3 cassandra-driver
pip3 install fabric
pip3 install flask
pip3 install wtforms

echo "INFO: python packages successfully installed"


