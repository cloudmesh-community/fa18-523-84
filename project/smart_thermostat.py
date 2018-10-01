# I523 Course Project
# Smart Thermostat

#Import packages
import os
import glob
import time
import pyowm
import geocoder
import pandas as pd
import datetime
from cassandra.cluster import Cluster

######################
# function to collect Weather Data
# Sources for this section:
# 	documentation for the open weather api python module: https://pyowm.readthedocs.io/en/latest/usage-examples.html#create-global-owm-object
# 	geocoder code copied from stackoverflow post by Apollo_LFB: https://stackoverflow.com/questions/24906833/get-your-location-through-python
# 	geocoder docs also used to understand the package usage: https://geocoder.readthedocs.io/ 
######################
def get_current_weather():
	g = geocoder.ip('me')
	owm = pyowm.OWM('enterAPI_key from owm')
	obs = owm.weather_at_coords(g.latlng[0],g.latlng[1])
	w = obs.get_weather()
	curr_weather_data = [w.get_reference_time(timeformat='date'), w.get_detailed_status(), w.get_temperature('fahrenheit')['temp']]
	curr_weather_df = pd.DataFrame([curr_weather_data], columns = ['Date and Time','Condition','Temp (F)'])
	return curr_weather_df


######################
# functions to get temperature data
# Sources for this section:
#   code in this section copied from:  http://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/ 
######################

def read_temp_raw():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


######################
# functions to send data to database
# Sources for this section:
#   code for pandas_factory function from: https://stackoverflow.com/questions/41247345/python-read-cassandra-data-into-pandas
#   documentation for cassandra cluster: https://datastax.github.io/python-driver/api/cassandra/cluster.html
######################

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

def read_cassandra_query(query, keyspace):
    cluster = Cluster()
	session = cluster.connect()
	session = cluster.connect( keyspace )
    session.row_factory = pandas_factory
	session.default_fetch_size = None
    rslt = session.execute( query )
    rslt_df = rslt._current_rows
    cluster.shutdown()
    return rslt_df


######################
# Output
######################

print(get_current_weather())
#print(read_temp())

g = geocoder.ip('me')
print(g.geojson)

#while True:
#  print(read_temp())  
#  time.sleep(1)
