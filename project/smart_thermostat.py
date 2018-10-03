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
#import pytz
#from tzwhere import tzwhere
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
	owm = pyowm.OWM('c38dcf6008303a9e9ff6464a5850e3ef')
	obs = owm.weather_at_coords(g.latlng[0],g.latlng[1])
	w = obs.get_weather()
	curr_weather_data = [w.get_reference_time(timeformat='date'), w.get_detailed_status(), w.get_temperature('fahrenheit')['temp']]
	#curr_weather_df = pd.DataFrame([curr_weather_data], columns = ['Date and Time','Condition','Temp (F)'])
	return curr_weather_data


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
#   documentation for cassandra cluster module: https://datastax.github.io/python-driver/api/cassandra/cluster.html
######################

def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)

def cassandra_query(keyspace, query, params=(), return_data=False, contact_points=['127.0.0.1'], port=9042):
	try:
		if return_data == True:
			cluster = Cluster( contact_points, port )
			session = cluster.connect( keyspace )
			session.row_factory = pandas_factory
			session.default_fetch_size = None
			rslt = session.execute( query )
			rslt_df = rslt._current_rows
			cluster.shutdown()
			return rslt_df
		else:
			cluster = Cluster( contact_points, port )
			session = cluster.connect( keyspace )
			session.execute( query, params )
			cluster.shutdown()
			return 'Data loaded to database'
	except AttributeError:
		raise


######################
# Output
######################

now = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
timeStampVal = get_current_weather()[0] - datetime.timedelta(hours=4) #convert to EST: Need to find a way to convert dynamically
condition = get_current_weather()[1]
out_temp_f = get_current_weather()[2]
in_temp_f = 71.2 
#in_temp_c, in_temp_f = read_temp()

insert_data = '''
            INSERT INTO temp_data (indoor_time, outdoor_time, out_condition, out_temp_f, in_temp_f)
            VALUES (%s,%s,%s,%s,%s)
            ''' 

params = (now,str(timeStampVal),condition,out_temp_f,in_temp_f)

print(cassandra_query('environment_data', insert_data, params))


#print(read_temp())

#g = geocoder.ip('me')
#print(g.geojson)

#while True:
#  print(read_temp())  
#  time.sleep(1)
