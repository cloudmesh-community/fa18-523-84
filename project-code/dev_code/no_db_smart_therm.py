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
#   LCD + DHT11:  http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/
#   GPIO: https://tutorials-raspberrypi.com/raspberry-pi-control-relay-switch-via-gpio/
#   Touch_Callback: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
######################

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#################
# HARD CODE PINS FOR SENSORS
RELAY_PIN_1 = 16
RELAY_PIN_2 = 18
TOUCH_PIN = 13
LIGHT_PIN = 11
TEMP_HUMID_PIN = 4 #This is the GPIO pin. Other pins set using BOARD
#################

GPIO.setup(RELAY_PIN_1, GPIO.OUT)
GPIO.setup(RELAY_PIN_2, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = CharLCD(cols=16,rows=2,pin_rs=37,pin_e=35,pins_data=[33,31,29,23],numbering_mode=GPIO.BOARD)

display_num = 1 # Sets the starting display.  Number will change with button press

def read_temp_humid():
	try:
		humid, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, TEMP_HUMID_PIN)
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return humid, temp_f
	except:
		return 0,0

def touch_callback(channel):
	global display_num
	if display_num == 1:
		if GPIO.input(TOUCH_PIN) == 1:
			display_num = 0
		else:
			display_num = 1
	else:
		if GPIO.input(TOUCH_PIN) == 1:
			display_num = 1
		else:
			display_num = 0

GPIO.add_event_detect(TOUCH_PIN, GPIO.RISING, callback=touch_callback)




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
# functions to adjust the temperature
# Sources for this section:
#   timezone offset: https://stackoverflow.com/questions/15742045/getting-time-zone-from-lat-long-coordinates
######################

def set_tolarance(start='08:00:00', end='22:30:00', main=1, secondary=5):
	start = datetime.datetime.strptime(start, '%H:%M:%S')
	end = datetime.datetime.strptime(end, '%H:%M:%S')
	#Adjust timezone
	tf = timezonefinder.TimezoneFinder()
	timezone_str = tf.certain_timezone_at(lat=g.latlng[0], lng=g.latlng[1])
	timezone = pytz.timezone(timezone_str)
	dt = datetime.datetime.utcnow()
	timezone.localize(dt)
	now = datetime.datetime.utcnow() + timezone.utcoffset(dt)

	# compare current time to start and end points
	if now > start and now < end:
		if GPIO.input(LIGHT_PIN) == 0:  # Check if the lights are on.  Indicates if someone is active.
			return main
		else:
			return secondary
	else:
		return main


def thermostat_adjust(indoor_temp, outdoor_temp, desired_temp=69, sys_off=False, fan_on=False, tolarance=2):
	if sys_off == True:
		GPIO.output(RELAY_PIN_1, GPIO.HIGH)
		GPIO.output(RELAY_PIN_2, GPIO.HIGH)
		return 'ALL OFF'
	elif sys_off == False and fan_on == True:
		if indoor_temp > desired_temp + tolarance and indoor_temp < outdoor_temp:
			GPIO.output(RELAY_PIN_2, GPIO.LOW)
			return 'AC ON'
		elif indoor_temp < desired_temp - tolarance and indoor_temp > outdoor_temp:
			GPIO.output(RELAY_PIN_1, GPIO.LOW)
			return 'HEAT ON'
		else:
			return 'FAN ON'
	else:
		if indoor_temp > desired_temp + tolarance and indoor_temp < outdoor_temp:
			GPIO.output(RELAY_PIN_2, GPIO.LOW)
			return 'AC ON'
		elif indoor_temp < desired_temp - tolarance and indoor_temp > outdoor_temp:
			GPIO.output(RELAY_PIN_1, GPIO.LOW)
			return 'HEAT ON'
		else:
			GPIO.output(RELAY_PIN_1, GPIO.HIGH)
			GPIO.output(RELAY_PIN_2, GPIO.HIGH)
			return 'SYS OFF'


######################
# Output
######################

#g = geocoder.ip('me')
#print(g.geojson)

while True:
	delay = 40
	while delay > 0:

		curr_weather = get_current_weather(g)

		# Automatic timezone adjustment code modified from: https://stackoverflow.com/questions/15742045/getting-time-zone-from-lat-long-coordinates
		tf = timezonefinder.TimezoneFinder()
		timezone_str = tf.certain_timezone_at(lat=g.latlng[0], lng=g.latlng[1])
		timezone = pytz.timezone(timezone_str)
		dt = datetime.datetime.utcnow()
		timezone.localize(dt)
		now = datetime.datetime.utcnow() + timezone.utcoffset(dt)
		timeStampVal = curr_weather[0] + timezone.utcoffset(dt)

		# Environment data variables
		condition = curr_weather[1]
		out_temp_f = curr_weather[2]
		in_humid, in_temp_f = read_temp_humid()

		# Adjust thermostat based on variables
		if in_temp_f is not None or out_temp_f is not None:
			output = thermostat_adjust(in_temp_f,out_temp_f,desired_temp=69.0,tolarance=set_tolarance())
			#print(output)
		else:
			pass

		# Record data in database
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
			lcd.write_string('In Humid: ' + str(in_humid) + '%')
		else:
			lcd.clear()
			lcd.cursor_pos = (0,0)
			lcd.write_string('Out Temp: ' + str(round(out_temp_f,1)) + 'F')
			lcd.cursor_pos = (1,0)
			lcd.write_string(str(condition[0:15]))

		time.sleep(15)
		delay = delay - 1

	print(str(now)+' | '+str(in_temp_f)+' | '+str(out_temp_f)+' | '+str(timeStampVal))
