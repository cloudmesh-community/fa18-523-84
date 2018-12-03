from flask import Flask, render_template, flash, request, make_response, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import psycopg2
from psycopg2.extensions import AsIs
from cassandra.cluster import Cluster
import pandas
import os
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import selenium
import datetime

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

#today's date used on multiple pages
dateVal = str(datetime.date.today())
dateVal = dateVal.replace('-','')

relativePath = os.getcwd()

class ReusableForm(Form):
    school = TextField('Institution Name:')
    compare = TextField('Institution Name:')
    name = TextField('Student Name:', validators=[validators.required(), validators.Length(min=1, max=35)])
    score = TextField('SAT / ACT Score:', validators=[validators.required(), validators.Length(min=1, max=35)])
 

def read_query(con, query, variables={}):
    cursor = con.cursor()
    cursor.arraysize = 5000
    try:
        cursor.execute( query, variables )
        print("Downloading query results...")
        names = [ x[0] for x in cursor.description]
        rows = cursor.fetchall()
        print("Writing query results to dataframe...")
        return pandas.DataFrame( rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()

def pandas_factory(colnames, rows):
    return pandas.DataFrame(rows, columns=colnames)

#initialize session for college_search keyspace
cluster = Cluster()
session = cluster.connect()
session = cluster.connect('college_search')

session.row_factory = pandas_factory
session.default_fetch_size = None

def read_cassandra_query(query):
    rslt = session.execute( query )
    rslt_df = rslt._current_rows
    print('\nResults for: '+query)
    return rslt_df


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
        name = request.form['name']
        score = request.form['score']
        score = score.replace(',','')

        if form.validate():
            # Save the comment here.
            now = datetime.datetime.utcnow()

            session.execute('''
            INSERT INTO user (timeStampVal,dateVal,name,score)
            VALUES (%s,%s,%s,%s)
            ''', (now,dateVal,name,score) )

            query = 'SELECT name FROM user WHERE dateVal = \''+dateVal+'\' ORDER BY timeStampVal DESC LIMIT 1'
            name_df = read_cassandra_query(query)

            flash('Thanks for the data '+name_df.iloc[0,0]+'!')
            return render_template('homepage2.html', url ='/static/images/state_univeristy.png', form=form)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('homepage2.html', url ='/static/images/state_univeristy.png', form=form)


@app.route("/LongTermIncome", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        school=request.form['school']
        if school=='':
            school = '%'
        else:
            pass
        order=request.form['order']

        con = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='Tbobitctsotw.1?2'")

        SQL = '''SELECT 
                INSTNM AS "Institution Name"
                ,SUM(CAST(coalesce(UG, '0') AS NUMERIC(8,2))) as "Undergraduate Enrollment"
                ,ROUND(SUM(CAST(coalesce(SAT_AVG, '0') AS NUMERIC(8,2))),0) as "Average SAT Score"
                ,SUM(CAST(coalesce(ADM_RATE_ALL, '0') AS NUMERIC(8,3))) as "Admission Rate"
                ,SUM(CAST(coalesce(COSTT4_A, '0') AS NUMERIC(8,2))) as "Average Cost per Year"
                ,SUM(CAST(coalesce(DEBT_MDN, '0') AS NUMERIC(8,2))) as "Median Student Debt"
                ,ROUND(SUM(CAST(coalesce(MN_EARN_WNE_P10, '0') AS NUMERIC(8,2))),0) as "Average Ten Year Income"
            FROM FEDERAL_HIGHER_ED
            WHERE INSTNM LIKE %(school)s
            GROUP BY
                INSTNM
            ORDER BY "%(order)s" DESC
        '''

        SQL_vars = {"school": '%'+str(school)+'%', "order": AsIs(order)}
        dataframe = read_query(con, SQL, variables=SQL_vars)

        #FORMAT DATAFRAME COLUMNS
        dataframe['Average Ten Year Income'] = dataframe['Average Ten Year Income'].map('${:,.0f}'.format)
        dataframe['Admission Rate'] = dataframe['Admission Rate'].map('{:,.1%}'.format)
        dataframe['Average Cost per Year'] = dataframe['Average Cost per Year'].map('${:,.0f}'.format)
        dataframe['Median Student Debt'] = dataframe['Median Student Debt'].map('${:,.0f}'.format)
        dataframe['Undergraduate Enrollment'] = dataframe['Undergraduate Enrollment'].map('{:,.0f}'.format)

        con.close()

        if school=='%':
            school_text = 'all institutions'
        else:
            school_text = school

        flash('Query result for ' + str(school_text) + ' ordered decending by ' + str(order))
        return render_template('LongTermIncome.html', tables=[dataframe.to_html(classes='result')], form=form)
             

    return render_template('LongTermIncome.html', form=form)
 


@app.route("/compare", methods=['GET', 'POST'])
def compare():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        compare=request.form['compare']

        con = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='Tbobitctsotw.1?2'")

        SQL = '''SELECT 
                INSTNM AS "Institution Name"
                ,ROUND(SUM(CAST(coalesce(COSTT4_A, '0') AS NUMERIC(8,2))),1) as "Average Cost per Year"
                ,ROUND(SUM(CAST(coalesce(DEBT_MDN, '0') AS NUMERIC(8,2))),1) as "Median Student Debt"
                ,ROUND(SUM(CAST(coalesce(MN_EARN_WNE_P10, '0') AS NUMERIC(8,2))),1) as "Average Ten Year Income"
            FROM FEDERAL_HIGHER_ED
            WHERE INSTNM = %(school)s
            GROUP BY
                INSTNM

            UNION ALL

            SELECT 
                'State Average' AS INSTNM
                ,ROUND(AVG(CAST(coalesce(COSTT4_A, '0') AS NUMERIC(8,2))),1) as "Average Cost per Year"
                ,ROUND(AVG(CAST(coalesce(DEBT_MDN, '0') AS NUMERIC(8,2))),1) as "Median Student Debt"
                ,ROUND(AVG(CAST(coalesce(MN_EARN_WNE_P10, '0') AS NUMERIC(8,2))),1) as "Average Ten Year Income"  
            FROM FEDERAL_HIGHER_ED
        '''

        SQL_vars = {"school": str(compare)}
        dataframe = read_query(con, SQL, variables=SQL_vars)

        
        alt.renderers.enable('notebook')

        dataframe['Average Cost per Year'] = dataframe['Average Cost per Year'].apply(pandas.to_numeric)
        dataframe['Median Student Debt'] = dataframe['Median Student Debt'].apply(pandas.to_numeric)
        dataframe['Average Ten Year Income'] = dataframe['Average Ten Year Income'].apply(pandas.to_numeric)

        dataframe2 = pandas.melt(dataframe, id_vars=['Institution Name'], value_vars=['Average Cost per Year', 'Median Student Debt','Average Ten Year Income'])

        #print(dataframe2)

        alt.Chart(dataframe2).mark_bar().encode(
            x=alt.X('Institution Name', scale=alt.Scale(rangeStep=75), axis=alt.Axis(title='')),
            y=alt.Y('value', axis=alt.Axis(title='$ USD', grid=False)),
            color=alt.Color('Institution Name', scale=alt.Scale(range=["#7c868d", "#659CCA"])),
            column='variable'
        ).configure_view(
            stroke='transparent'
        ).configure_axis(
            domainWidth=0.8
        ).save(relativePath+'\\static\\images\\compare.png')

        con.close()

        return render_template('compare.html', url ='/static/images/compare.png', form=form)
            
    return render_template('compare.html', url ='/static/images/compare.png', form=form)


@app.route("/what_school", methods=['GET', 'POST'])
def what_school():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        
        #CASSANDRA QUERY TO GET USER SCORE
        query = 'SELECT name, score FROM user WHERE dateVal = \''+dateVal+'\' ORDER BY timeStampVal DESC LIMIT 1'
        out_df = read_cassandra_query(query)
        out_df.columns = ['Name','SAT_Score']

        outName = out_df.iloc[0,0]
        outScore = out_df.iloc[0,1]

        #SQL QUERY TO GET SCHOOL AVERAGES
        con = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='Tbobitctsotw.1?2'")

        SQL = '''SELECT 
                INSTNM AS "Name"
                ,ROUND(SUM(CAST(coalesce(SAT_AVG, '0') AS NUMERIC(8,2))),0) as "SAT_Score"
            FROM FEDERAL_HIGHER_ED
            GROUP BY
                INSTNM
        '''

        dataframe = read_query(con, SQL)

        con.close()

        #combine dataframes to render chart
        chart_data = dataframe.append(out_df.head(1), sort=False, ignore_index=True)

        chart_data['SAT_Score'] = chart_data['SAT_Score'].apply(pandas.to_numeric)
        chart_data.sort_values(by='SAT_Score')
        chart_data = chart_data[chart_data.SAT_Score != 0]

        alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Name:O", axis=alt.Axis(title='School Names'), sort=alt.SortField(field='SAT_Score', order='ascending', op='sum') ),
            y=alt.Y("sum(SAT_Score):Q", axis=alt.Axis(title='Average SAT Score') ),
            # The highlight will be set on the result of a conditional statement
            color=alt.condition(
                alt.datum.Name == outName,  # If the year is 1970 this test returns True,
                alt.value('orange'),     # which sets the bar orange.
                alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
            )
        ).save(relativePath+'\\static\\images\\what_school.png')


        flash('Hi ' + str(outName) + ' here is a chart of your best options with an SAT score of ' + str(outScore))
        return render_template('what_school.html', url ='/static/images/what_school.png', form=form)     

    return render_template('what_school.html', url ='/static/images/what_school.png', form=form)



if __name__ == "__main__":
    app.run()
