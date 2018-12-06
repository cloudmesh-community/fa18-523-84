# Smart Thermostat Control Center

from flask import Flask, render_template, flash, request, make_response, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import numpy as np
import time
import datetime
import pytz
import timezonefinder
import geocoder
import altair as alt

relativePath = os.getcwd()

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

@app.route("/", methods=['GET', 'POST'])
def index():
	form = ReusableForm(request.form)

	#get current status from status table
	status = 'SELECT * FROM therm_status'
	status_df = cassandra_query('smart_therm', status, return_data=True, contact_points=['10.0.0.42'], port=9042)

	#get most recent readings. need to get max date key first and convert to unix
	get_max = 'SELECT max(indoor_time) AS max_time FROM therm_data'
	max_df = cassandra_query('smart_therm', get_max, return_data=True, contact_points=['10.0.0.42'], port=9042)
	max_time = max_df.iloc[0]['max_time']
	max_time_unix = max_time.value // 10 ** 6

	#get unix date from 30 days ago to show the chart
	trailing30 = max_df.iloc[0]['max_time'] - pd.to_timedelta(30, unit='d')
	trailing30_unix = trailing30.value // 10 ** 6

	get_data = 'SELECT * FROM therm_data WHERE indoor_time = '+str(max_time_unix)
	data_df = cassandra_query('smart_therm', get_data, return_data=True, contact_points=['10.0.0.42'], port=9042)

	chart_data = 'SELECT * FROM therm_data WHERE indoor_time >= '+str(trailing30_unix)+'ALLOW FILTERING'
	chart_df = cassandra_query('smart_therm', chart_data, return_data=True, contact_points=['10.0.0.42'], port=9042)

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

	#############################
	# chart code

	chart_df['system_status'] = np.where(chart_df['status']=='SYS OFF', 0, 1)
	df2 = pd.melt(chart_df, id_vars=['indoor_time'], value_vars=['in_temp_f','out_temp_f'])

	alt.Chart(df2).mark_area(opacity=0.6).encode(
		x="indoor_time:T",
		y=alt.Y("value:Q", stack=None),
		color='variable:N'
	).properties(height=200, width=600).save(relativePath+'\\static\\images\\chart1.png')

	alt.Chart(chart_df).mark_area().encode(
	    alt.X('indoor_time:T'),
	    alt.Y('system_status:Q', scale=alt.Scale(domain=(0, 2)))
	).properties(height=100, width=600).save(relativePath+'\\static\\images\\chart2.png')

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
			print(update_status)
			cassandra_query('smart_therm', update_status, return_data=False, contact_points=['10.0.0.42'], port=9042)

			flash('Updated Thermostat Settings')
			return render_template('homepage.html', img1='/static/images/chart1.png', img2='/static/images/chart2.png', form=form, username=username, update_time=update_time, humid=humid, in_temp_f=in_temp_f, out_temp_f=out_temp_f, condition=condition, status=status, fan_on=fan_on, sys_off=sys_off, desired_temp=desired_temp)
		else:
			flash('Error: All the form fields are required. ')

	return render_template('homepage.html', img1='/static/images/chart1.png', img2='/static/images/chart2.png', form=form, username=username, update_time=update_time, humid=humid, in_temp_f=in_temp_f, out_temp_f=out_temp_f, condition=condition, status=status, fan_on=fan_on, sys_off=sys_off, desired_temp=desired_temp)


if __name__ == '__main__':
	app.run()
