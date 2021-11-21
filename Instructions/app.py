from sqlalchemy import engine
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
import datetime as dt

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station


@app.route("/")
def home():
    return(
        f"Welcome to my 'Home' page!<br>"
        f"All routes<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start <br>"
        f"/api/v1.0/start/end") 
           


@app.route("/api/v1.0/precipitation")
def precipitation():
    my_session=Session(engine)
    precipitation_result=my_session.query(Measurement.date,Measurement.prcp).all()
    all_precipitation = []
    for date,prcp in precipitation_result:
        date_d={}
        date_d[date]=prcp
        all_precipitation.append(date_d)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    my_session=Session(engine)
    stations_result=my_session.query(Station.station).all()
    all_stations = list(np.ravel(stations_result))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    my_session=Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_result=my_session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date>=query_date,Measurement.station=='USC00519281').all()
    all_tobs = list(np.ravel(tobs_result))
    return jsonify(all_tobs)





@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start,end=None):
    my_session=Session(engine)
    start_date_result=my_session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))

    if start:
        startdate_result = start_date_result.filter(Measurement.date >= start)

    if end:
        startdate_result = start_date_result.filter(Measurement.date <= end)

    results = start_date_result.all()[0]

    keys = ["Min Temp", "Max Temp", "Avg Temp"]

    temp_dict = {keys[i]: results[i] for i in range(len(keys))}

    return jsonify(temp_dict)




if __name__ == "__main__":
    app.run(debug=True)