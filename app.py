#Dependencies 
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, inspect, func, desc
from sqlalchemy import distinct
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station 
app = Flask(__name__)

@app.route("/")
def homeStation():
    
    return ( 
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/put date here<br/>"
        f"/api/v1.0/put date here/put the other date here<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    dateQuery = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= dateQuery).all()

    session.close()    

    precip = []
    for date, prcp in results: 
         precipDict = {}
         precipDict["date"] = date 
         precipDict["prcp"] = prcp 
         precip.append(precipDict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    resultInfo = session.query(station.name, func.count(measurement.station)).\
        filter(measurement.station == station.station).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()

    stationsList = list(np.ravel(resultInfo))

    session.close()    

    return jsonify(stationsList)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    dateQuery = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).\
    filter(measurement.date >= dateQuery).\
    filter(measurement.station == "USC00519281").all()

    session.close()    

    tobs1 = list(np.ravel(results))

    return jsonify(tobs1)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)
    
    starting = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

        

    session.close()  

    return jsonify(starting)


@app.route("/api/v1.0/<start_date>/<end_date>")
def range(start_date, end_date):

    session = Session(engine)
    startEndDate = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()

    return jsonify(startEndDate)

#closing statement
if __name__=="__main__":
    app.run(debug=True)