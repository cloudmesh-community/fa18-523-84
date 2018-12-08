# Smart Thermostat Control Center
# Sources: https://github.com/bokeh/bokeh/blob/1.0.2/examples/embed/json_item.py
# https://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html
# http://flask.pocoo.org/docs/1.0/

from flask import Flask, render_template, flash, request, make_response, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import os
from cassandra.cluster import Cluster
import pandas as pd
import numpy as np
import time
import datetime
import pytz
import timezonefinder
import geocoder
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.sampledata.iris import flowers
from jinja2 import Template
import json

relativePath = os.getcwd()
cassandra_contact_points = ['10.0.0.42']

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

g = geocoder.ip('me')
tf = timezonefinder.TimezoneFinder()
timezone_str = tf.certain_timezone_at(lat=g.latlng[0], lng=g.latlng[1])
timezone = pytz.timezone(timezone_str)
dt = datetime.datetime.utcnow()
timezone.localize(dt)

def pandas_factory(colnames, rows):
	return pd.DataFrame(rows, columns=colnames)

def cassandra_query(keyspace, query, params=(), return_data=False, contact_points=['127.0.0.1'], port=9042):
	try:
		if return_data == True:
			cluster = Cluster( contact_points=contact_points, port=port )
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
		print('ERROR: query failed')


class ReusableForm(Form):
	user = TextField('Username:', validators=[validators.required(), validators.Length(min=1, max=35)])
	#password = TextField('Password:', validators=[validators.required(), validators.Length(min=1, max=35)])
	desired_temp = TextField('Desired Temperature:', validators=[validators.required(), validators.Length(min=1, max=35)])
	#main = TextField('Main Temperature Range:')
	#secondary = TextField('Secondary Temperature Range:')

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Smart Thermostat Control Center</title>
  <link rel="stylesheet" media="screen" href ="static/bootstrap.min.css">
  <link rel="stylesheet" href="static/bootstrap-theme.min.css">
  {{ resources }}
  <meta name="viewport" content = "width=device-width, initial-scale=1.0">

    <style type="text/css">
    
      body {padding-top: 70px;}

      table.dataframe, .dataframe th, .dataframe td {
        border: none;
        border-bottom: 2px solid #C8C8C8;
        border-collapse: collapse;
        text-align:left;
        padding: 10px;
        margin-bottom: 40px;
        font-size: 0.9em;
        
      }

      .centerText{ 
        text-align:center;
        padding: 0px;
      }

      img {
        max-width: 100%;
      }

      img.align-self {
        align-self: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
      }

      .result th {
        background-color: #00A1E0;
        color: white;
      }

      tr:nth-child(odd)   td { background-color:#eee; }
      tr:nth-child(even)  td { background-color:#fff; }
      tr:hover            td { background-color: #ffff99;}
    </style>
</head>
<body>
    <div class="container">
      <h1 class="centerText">Smart Thermostat Control Center</h1>
      <br>
      <h4 class="centerText">
        Settings last updated by {{ username }} at {{ update_time }} <br />
        {{ message }}
      </h4>
      <p class="centerText">
        System Status: {{ sys_off }} <br />
        Fan: {{ fan_on }} <br />
        Temp: {{ desired_temp }}
      </p>
      <br>
      <div>
        <h2 class="centerText">Current System Statistics</h2>
        <p class="centerText">
        System Status: {{ status }} <br />
        Indoor Temp: {{ in_temp_f }} <br />
        Indoor Humidity: {{ humid }} <br />
        Outdoor Temp: {{ out_temp_f }} <br /> 
        Conditions: {{ condition }} <br />
        </p>
    </div>
	<div id="myplot" class="centerText">
		<script>
		fetch('/plot')
			.then(function(response) { return response.json(); })
			.then(function(item) { Bokeh.embed.embed_item(item); })
		</script>
	</div>
	<h2>Change Thermostat Settings</h2>
      <br>
      <form  action="" method="post" role="form">
        <div class="form-group">
            <label for="user">Username:</label>
            <input type="text" class="form-control" id="user" name="user" placeholder="Please enter your username">
        </div>
        <div class="dropdown">
          <label for="system">System Status:</label>
          <select name= "system" method="GET" id="system" action="/">
              <option selected>On</option>
              <option>Off</option>
          </select>
        </div>
        <div class="dropdown">
          <label for="fan">Fan Status:</label>
          <select name= "fan" method="GET" id="fan" action="/">
              <option selected>Off</option>
              <option>On</option>
          </select>
        </div>
        <div class="form-group">
            <label for="desired_temp">Desired Temperature:</label>
            <input type="text" class="form-control" id="desired_temp" name="desired_temp" placeholder="Please enter your desired temperature">
            <br>
            <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
      <br>
    </div>
</body>
""")

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

def make_plot(x, y):
    p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p

@app.route('/', methods=['GET', 'POST'])
def root():
	form = ReusableForm(request.form)
	message = ''

	#get current status from status table
	status = 'SELECT * FROM therm_status'
	status_df = cassandra_query('smart_therm', status, return_data=True, contact_points=cassandra_contact_points, port=9042)

	#get most recent readings. need to get max date key first and convert to unix
	get_max = 'SELECT max(indoor_time) AS max_time FROM therm_data'
	max_df = cassandra_query('smart_therm', get_max, return_data=True, contact_points=cassandra_contact_points, port=9042)
	max_time = max_df.iloc[0]['max_time']
	max_time_unix = max_time.value // 10 ** 6

	#get unix date from 30 days ago to show the chart
	trailing30 = max_df.iloc[0]['max_time'] - pd.to_timedelta(30, unit='d')
	trailing30_unix = trailing30.value // 10 ** 6

	get_data = 'SELECT * FROM therm_data WHERE indoor_time = '+str(max_time_unix)
	data_df = cassandra_query('smart_therm', get_data, return_data=True, contact_points=cassandra_contact_points, port=9042)

	############################
	# Variables from data tables

	#data variables
	humid = data_df.iloc[0]['humidity']
	in_temp_f = data_df.iloc[0]['in_temp_f']
	out_temp_f = data_df.iloc[0]['out_temp_f']
	condition = data_df.iloc[0]['out_condition']
	status = data_df.iloc[0]['status']
	
	#status variables
	desired_temp = status_df.iloc[0]['desired_temp']
	fan_on = status_df.iloc[0]['fan_on']
	#main = current_vars_df.iloc[0]['main']
	#secondary = current_vars_df.iloc[0]['secondary']
	sys_off = status_df.iloc[0]['sys_off']
	username = status_df.iloc[0]['username']
	update_time = status_df.iloc[0]['update_time']

	#print(form.errors)
	if request.method == 'POST':
		new_user = request.form['user']
		#password = request.form['password']
		new_desired_temp = request.form['desired_temp']
		#new_main = request.form['main']
		#new_secondary = request.form['secondary']
		new_sys_off = request.form['system']
		new_fan_on = request.form['fan']

		if new_sys_off == 'Off':
			new_sys_off = 'True'
		else:
			new_sys_off = 'False'

		if new_fan_on == 'On':
			new_fan_on = 'True'
		else:
			new_fan_on = 'False'

		new_desired_temp = float(new_desired_temp)

		if form.validate():
			# Save the comment here.
			now = datetime.datetime.utcnow() + timezone.utcoffset(dt)
			now_df = pandas_factory(['timestamp'],[now])
			now_unix = now_df.iloc[0]['timestamp'].value // 10 ** 6
			update_time = now_df.iloc[0]['timestamp']

			if new_desired_temp != desired_temp and new_desired_temp >= 65 and new_desired_temp <= 80:
				desired_temp = new_desired_temp
			
			if new_sys_off != sys_off:
				sys_off = new_sys_off
			
			if new_fan_on != fan_on:
				fan_on = new_fan_on
			
			if username != new_user:
				username = new_user

			update_status = 'UPDATE therm_status SET desired_temp='+str(desired_temp)+', fan_on=\''+fan_on+'\', sys_off=\''+sys_off+'\', update_time=\''+str(now_unix)+'\', username=\''+username+'\' WHERE key = 1'
			cassandra_query('smart_therm', update_status, return_data=False, contact_points=cassandra_contact_points, port=9042)

			message = 'SUCCESS: Updated Thermostat Settings'
			return page.render(resources=CDN.render(), message=message, form=form, username=username, update_time=update_time, humid=humid, in_temp_f=in_temp_f, out_temp_f=out_temp_f, condition=condition, status=status, fan_on=fan_on, sys_off=sys_off, desired_temp=desired_temp)
		else:
			message = 'ERROR: fill out all fields'
			return page.render(resources=CDN.render(), message=message, form=form, username=username, update_time=update_time, humid=humid, in_temp_f=in_temp_f, out_temp_f=out_temp_f, condition=condition, status=status, fan_on=fan_on, sys_off=sys_off, desired_temp=desired_temp)

	return page.render(resources=CDN.render(), message=message, form=form, username=username, update_time=update_time, humid=humid, in_temp_f=in_temp_f, out_temp_f=out_temp_f, condition=condition, status=status, fan_on=fan_on, sys_off=sys_off, desired_temp=desired_temp)

@app.route('/plot')
def plot():
	#get most recent readings. need to get max date key first and convert to unix
	get_max = 'SELECT max(indoor_time) AS max_time FROM therm_data'
	max_df = cassandra_query('smart_therm', get_max, return_data=True, contact_points=cassandra_contact_points, port=9042)
	max_time = max_df.iloc[0]['max_time']
	max_time_unix = max_time.value // 10 ** 6

	#get unix date from 30 days ago to show the chart
	trailing30 = max_df.iloc[0]['max_time'] - pd.to_timedelta(30, unit='d')
	trailing30_unix = trailing30.value // 10 ** 6

	chart_data = 'SELECT * FROM therm_data WHERE indoor_time >= '+str(trailing30_unix)+'ALLOW FILTERING'
	chart_df = cassandra_query('smart_therm', chart_data, return_data=True, contact_points=cassandra_contact_points, port=9042)

	#############################
	# chart code

	chart_df['system_status'] = np.where(chart_df['status']=='SYS OFF', 0, 1)
	chart_df = chart_df.sort_values(by=['indoor_time'])

	p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
	p.line(chart_df['indoor_time'], chart_df['in_temp_f'], color='navy', alpha=1)
	p.line(chart_df['indoor_time'], chart_df['out_temp_f'], color='orange', alpha=1)
	
	return json.dumps(json_item(p, "myplot"))


if __name__ == '__main__':
	app.run()
