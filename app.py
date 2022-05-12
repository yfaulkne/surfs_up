#Import dependencies

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Create the database engine

engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into classes

Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to each table
#Create a variable for each class to refernce later

Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link from Python to database

session = Session(engine)

#Create an instance using the magic method (__name__)
#Create a Flask application called app

app = Flask(__name__)

#Create the first route aka root (homepage)
@app.route('/')

#Create a function 'welcome'
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Create a route for precipitation

@app.route("/api/v1.0/precipitation")

#Create a function precipitation

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


#Create a route for stations

@app.route("/api/v1.0/stations")

#Create a stations function

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Create a route for temperature observations

@app.route("/api/v1.0/tobs")

#Create a temperature observations function

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Create a route for start/end date statistics report 

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Create a stats function

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)