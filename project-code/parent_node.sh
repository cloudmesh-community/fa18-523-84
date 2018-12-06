#!/bin/bash

#update / upgrade
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

echo "INFO: updates complete"

#install nmap for networking
sudo apt-get install nmap -y
#install and set up apache web server
#sources: https://www.youtube.com/watch?v=iVGtJOC71Fw
sudo apt-get install apache2 -y
sudo apt-get remove libapache2-mod-python libapache2-mod-wsgi -y
sudo apt-get install libapache2-mod-wsgi-py3 -y
sudo a2enmod wsgi -y

echo "INFO: tools and dependancies installed"

#install python packages
sudo apt-get install python3-pip
sudo apt-get install python3-pandas
sudo easy_install3 cassandra-driver
sudo pip3 install fabric
sudo pip3 install flask
sudo pip3 install wtforms
sudo pip3 install altair

echo "INFO: python packages successfully installed"

#install cassandra on the parent node
#Sources: https://www.linode.com/docs/databases/cassandra/deploy-scalable-cassandra/
sudo apt install software-properties-common -y
sudo apt-get purge openjdk*
sudo apt-get install openjdk-8-jdk -y
java -version


