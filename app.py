  
#Create Dependencies
import numpy as np
import datetime as dt

#Create Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect


#Import Flask
from flask import Flask, jsonify

#################################################
# DATABASE SET UP
#################################################
#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect Database as a new model
Base = automap_base()
#Reflect tables 
Base.prepare(engine, reflect = True)

#View all classes that automap found
#Base.classes.keys()

#Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session or link from python to our Data Base
session = Session(engine)

#################################################
# FLASK SET UP
#################################################
#Setup Flask
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
"""HOME OR INDEX ROUTE"""
#Home page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Homepage<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

#List all routes that are available
# Precipitation Route. /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
     
# Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value    
def precipitation():
        # Create our session (link) from Python to the DB
        session = Session(engine)
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        """Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting 
        only the `date` and `prcp` Values"""
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_dict = dict(prcp_data)
        
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_dict)


# Station Route. /api/v1.0/stations
@app.route("/api/v1.0/stations")

def stations():
        # Create our session (link) from Python to the DB
        session = Session(engine)
        # Return a JSON List of Stations From the Dataset
        stations = session.query(Station.station, Station.name).all()
        #Return a JSON list of stations from the dataset.
        return jsonify(stations)
        #?


# TOBs Route. /api/v1.0/tobs
#Query the dates and temperature observations of the most active station for the last year of data
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
        
        session = Session(engine)
        stations_obs = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        most_active_station = 'USC00519281'
        station_tobs = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= one_year_ago).\
            filter(Measurement.station == most_active_station).all()
        
        station_list = list(np.ravel(station_tobs))


        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(station_list)


# Start Day Route. /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def start_day(start):
        # Create our session (link) from Python to the DB
        session = Session(engine)
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(np.ravel(start_day))


        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)


# Start-End Day Route. /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        # Create our session (link) from Python to the DB
        session = Session(engine)
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(np.ravel(start_end_day))


        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)


# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)



#def precipitation():
    #precipitation_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
    #filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all
    #prcp_dict={}
    #prcp_dict = [{element[0]:element[1]} for element in precipitation_data]
    #return jsonify(prcp_dict)




