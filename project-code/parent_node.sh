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
sudo a2enmod wsgi
sudo apt install libatlas3-base #used for numpy issue source = https://www.raspberrypi.org/forums/viewtopic.php?t=207058

echo "INFO: tools and dependancies installed"

#install python packages
sudo apt-get install python3-pip
sudo apt-get install python3-pandas
sudo pip3 install fabric
sudo pip3 install flask
sudo pip3 install wtforms
sudo pip3 install timezonefinder
sudo pip3 install geocoder
sudo pip3 install bokeh
sudo easy_install3 cassandra-driver #this step takes a long time. I suggest ordering pizza :)

echo "INFO: python packages successfully installed"

#install cassandra on the parent node
#Sources: https://www.linode.com/docs/databases/cassandra/deploy-scalable-cassandra/
sudo apt install software-properties-common -y
sudo apt-get purge openjdk*
sudo apt-get install openjdk-8-jdk -y
java -version

wget "https://www-us.apache.org/dist/cassandra/3.11.3/apache-cassandra-3.11.3-bin.tar.gz"
tar -xvf apache-cassandra-3.11.3-bin.tar.gz
cd git-repos/fa18-523-84/project-code && git pull
sudo cp ~/git-repos/fa18-523-84/project-code/cassandra_custom.yaml ~/apache-cassandra-3.11.3/conf/cassandra_custom.yaml
sudo mv ~/apache-cassandra-3.11.3/conf/cassandra.yaml ~/
sudo mv ~/apache-cassandra-3.11.3/conf/cassandra-topology.properties ~/
sudo mv ~/apache-cassandra-3.11.3/conf/cassandra_custom.yaml ~/apache-cassandra-3.11.3/conf/cassandra.yaml


#Addiitonal manual cassandra config must be competed before starting cassandra
#first change the listen_address and the rpc_address on each node

#then start seed nodes first
cd apache-cassandra-3.11.3
bin/cassandra

#Cassandra sources:
#https://docs.datastax.com/en/cassandra/3.0/cassandra/initialize/initSingleDS.html
#https://cassandra.apache.org/doc/latest/configuration/cassandra_config_file.html
#https://stackoverflow.com/questions/29323709/unable-to-start-cassandra-node-already-exists

echo "INFO: cassandra installation complete - THERE ARE STILL MANUAL STEPS TO START CLUSTER"

#setup apache webserver
sudo cp -r ~/git-repos/fa18-523-84/project-code/FlaskApp ~/var/www/FlaskApp
sudo cp ~/git-repos/fa18-523-84/project-code/FlaskApp.conf ~/etc/apache2/sites-available/FlaskApp.conf
sudo a2ensite FlaskApp.conf
sudo /etc/init.d/apache2 restart

echo "INFO: apache webserver has been configured"

echo "INFO: parent node setup complete"
