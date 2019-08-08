import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes for climate Analysis!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > last_year).all()
    all_tobs = []

    for date_ob in results:
        all_tobs_dict = {}
        all_tobs_dict["Date"] = date_ob.date
        all_tobs_dict["Temperature"]=date_ob.tobs

        all_tobs.append(all_tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/stations")
def station():
    station_results = session.query(Station.station).all()
    station_list = list(np.ravel(station_results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_result = session.query(Measurement.date, Measurement.tob).filter(Measurement.date > last_year).all()
    tobs_list = list(np.ravel(tobs_result))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def StartDate(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    summary_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date)
    summary = list(np.ravel(summary_stats))
    return jsonify(summary)

@app.route("/api/v1.0/<start>/<end>")
def EndDate(start,end):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    summary_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start_date,end_date)).all()
    summary = list(np.ravel(summary_stats))
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)




