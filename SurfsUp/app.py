# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(bind=engine)

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
    
    precipitation_dict = {date: prcp for date, prcp in precipitation_scores}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(bind=engine)

    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    stations_list = [row[0] for row in most_active_stations]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(bind=engine)

    most_active_station_id = 'USC00519281'
    low_high_avg_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station_id).all()
    most_active_station_tob_data = [tob[0] for tob in low_high_avg_temp]

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= one_year_ago).all()
    tobs_list = [tob[0] for tob in tobs_data]

# I was not 100% sure if the instructions called for the most active station or a list of all the TOBS data, so I went ahead and included both.

    response = {
        "most_active_station_tob_data": most_active_station_tob_data,
        "tobs_list": tobs_list
    }

    return jsonify(response)

@app.route("/api/v1.0/<start>")
def start_route(start):
    session = Session(bind=engine)

    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid start date format, use YYYY-MM-DD"}), 400
    
    end_date = session.query(func.max(Measurement.date)).scalar()
    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temperatures = {
        "TMIN": result[0][0],
        "TMAX": result[0][1],
        "TAVG": result[0][2]
    }

    return jsonify(temperatures)

@app.route("/api/v1.0/<start>/<end>")
def start_end_route(start, end):
    session = Session(bind=engine)

    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temperatures = {
        "TMIN": result[0][0],
        "TMAX": result[0][1],
        "TAVG": result[0][2]
    }
    
    return jsonify(temperatures)

if __name__ == "__main__":
    app.run(debug=True)
