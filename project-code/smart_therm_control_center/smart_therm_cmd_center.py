# Smart Thermostat Control Center

from flask import Flask, render_template, flash, request, make_response, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    user = TextField('Username:', validators=[validators.required(), validators.Length(min=1, max=35)])
    #password = TextField('Password:', validators=[validators.required(), validators.Length(min=1, max=35)])
    desired_temp = TextField('Desired Temperature:')
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

    print(form.errors)
    if request.method == 'POST':
        user = request.form['user']
        #password = request.form['password']
        desired_temp = request.form['desired_temp']
        #main = request.form['main']
        #secondary = request.form['secondary']
        sys_off = request.form['system']
        fan_on = request.form['fan']

        if form.validate():
            # Save the comment here.

            flash('Updated Thermostat Settings')
            return render_template('homepage.html', url ='/static/images/thermostat_data.png', form=form)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('homepage.html', url ='/static/images/thermostat_data.png', form=form)


if __name__ == '__main__':
        app.run()
