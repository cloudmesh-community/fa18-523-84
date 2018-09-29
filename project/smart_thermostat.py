# I523 Course Project
# Smart Thermostat

#Import packages
from weather import Weather, Unit
import geocoder
import pandas as pd
import datetime

######################
# Collect Weather Data
# Sources for this section:
# 	weather API documentation on pypi.org: https://pypi.org/project/weather-api/
# 	geocoder code copied from stackoverflow post by Apollo_LFB: https://stackoverflow.com/questions/24906833/get-your-location-through-python
# 	geocoder docs also used to understand the package usage: https://geocoder.readthedocs.io/ 
######################
weather = Weather(unit=Unit.FAHRENHEIT) #set units
g = geocoder.ip('me')
#print(g.geojson)
location = weather.lookup_by_location(g.city)
forecast = location.forecast

today_date = str(datetime.date.today())
col_names = ['snap_date','fcst_date','condition','high','low']
weather_data = []
for f in forecast:
	weather_data.append([today_date,f.date,f.text,f.high,f.low]) 

weather_df = pd.DataFrame(weather_data, columns = col_names)

print(weather_df)
