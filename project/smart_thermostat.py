# I523 Course Project
# Smart Thermostat

#Import packages
import pyowm
import geocoder
import pandas as pd
import datetime

######################
# Collect Weather Data
# Sources for this section:
# 	documentation for the open weather api python module: https://pyowm.readthedocs.io/en/latest/usage-examples.html#create-global-owm-object
# 	geocoder code copied from stackoverflow post by Apollo_LFB: https://stackoverflow.com/questions/24906833/get-your-location-through-python
# 	geocoder docs also used to understand the package usage: https://geocoder.readthedocs.io/ 
######################
g = geocoder.ip('me')
#print(g.geojson)

owm = pyowm.OWM('c38dcf6008303a9e9ff6464a5850e3ef')
#obs = owm.weather_at_place(g.city)
obs = owm.weather_at_coords(g.latlng[0],g.latlng[1])
w = obs.get_weather()
curr_weather_data = [w.get_reference_time(timeformat='date'), w.get_detailed_status(), w.get_temperature('fahrenheit')['temp']]
curr_weather_df = pd.DataFrame([curr_weather_data], columns = ['Date and Time','Condition','Temp (F)'])
print(curr_weather_df)
