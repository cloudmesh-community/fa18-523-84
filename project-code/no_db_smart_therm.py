
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
import sys
import Adafruit_DHT
import pytz
import timezonefinder
from cassandra.cluster import Cluster
from RPLCD import CharLCD
from RPi import GPIO

######################
# function to collect Weather Data
# Sources for this section:
# 	documentation for the open weather api python module: https://pyowm.readthedocs.io/en/latest/usage-examples.html#create-global-owm-object
# 	geocoder code copied from stackoverflow post by Apollo_LFB: https://stackoverflow.com/questions/24906833/get-your-location-through-python
# 	geocoder docs also used to understand the package usage: https://geocoder.readthedocs.io/
######################

g = geocoder.ip('me')

def get_current_weather(g):
	owm = pyowm.OWM('24a35d03fca238fc68c5a56406696e20')
	obs = owm.weather_at_coords(g.latlng[0],g.latlng[1])
	w = obs.get_weather()
	curr_weather_data = [w.get_reference_time(timeformat='date'), w.get_detailed_status(), w.get_temperature('fahrenheit')['temp']]
	return curr_weather_data


######################
# functions to get temperature data and LCD setup
# Sources for this section:
#   code in this section copied from:  http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/ 
######################

GPIO.setwarnings(False)

lcd = CharLCD(cols=16,rows=2,pin_rs=37,pin_e=35,pins_data=[33,31,29,23],numbering_mode=GPIO.BOARD)
sensor = Adafruit_DHT.DHT11
pin = 4


def read_temp_humid():
	try:
		humid, temp_c = Adafruit_DHT.read_retry(sensor, pin)
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return humid, temp_f
	except:
		return 0,0



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
	except:
		print('Data not loaded. Check for Error')


######################
# Output
######################

#g = geocoder.ip('me')
#print(g.geojson)

while True:
	delay = 40
	display_num = 1
	while delay > 0:

		curr_weather = get_current_weather(g)

		# Automatic timezone adjustment code modified from: https://stackoverflow.com/questions/15742045/getting-time-zone-from-lat-long-coordinates
		tf = timezonefinder.TimezoneFinder()
		timezone_str = tf.certain_timezone_at(lat=g.latlng[0], lng=g.latlng[1])
		timezone = pytz.timezone(timezone_str)
		dt = datetime.datetime.utcnow()
		now = datetime.datetime.utcnow() + timezone.utcoffset(dt)
		timeStampVal = curr_weather[0] + timezone.utcoffset(dt)

		# Environment data variables
		condition = curr_weather[1]
		out_temp_f = curr_weather[2]
		in_humid, in_temp_f = read_temp_humid()

		insert_data = '''
	            INSERT INTO temp_data (indoor_time, outdoor_time, out_condition, out_temp_f, in_temp_f, humidity)
        	    VALUES (%s,%s,%s,%s,%s,%s)
	            '''

		params = (now,str(timeStampVal),condition,out_temp_f,in_temp_f,in_humid)

		#cassandra_query('environment_data', insert_data, params)

		if display_num == 1:
			lcd.clear()
			lcd.cursor_pos = (0,0)
			lcd.write_string('In Temp: ' + str(round(in_temp_f,1)) + 'F')
			lcd.cursor_pos = (1,0)
			lcd.write_string('Out Temp: ' + str(round(out_temp_f,1)) + 'F')
			display_num = 0
		else:
			lcd.clear()
			lcd.cursor_pos = (0,0)
			lcd.write_string('In Humid: ' + str(in_humid) + '%')
			lcd.cursor_pos = (1,0)
			lcd.write_string('Out Temp: ' + str(round(out_temp_f,1)) + 'F')
			display_num = 1

		time.sleep(15)
		delay = delay - 1

	print(str(now)+' | '+str(in_temp_f)+' | '+str(out_temp_f)+' | '+str(timeStampVal))
