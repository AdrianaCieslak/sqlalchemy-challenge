import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    max_date = session.query(func.max(Measurement.date)).all()[0][0]
    max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
    query_date = max_date - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > query_date).all()

    session.close()
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    station_temp = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= station_temp).all()
    
    session.close()

    temp = list(np.ravel(results))
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)