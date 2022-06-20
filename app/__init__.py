# External Imports
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy, inspect
import json
from flask_login import LoginManager
from datetime import timedelta
from datetime import datetime
from dateutil import tz
import pytz
from os import environ

# Flask app Setup
app = Flask(__name__)
app.config.from_file('config.json',load=json.load)

login_mgr = LoginManager(app)
login_mgr.login_view = 'login'
login_mgr.refresh_view = 'relogin'
login_mgr.needs_refresh_message = (u"Session timedout, please re-login")
login_mgr.needs_refresh_message_category = "info"
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Database Setup

db = SQLAlchemy(app)
app.SQLALCHEMY_TRACK_MODIFICATIONS=False

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models.models import User, mqtt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .setup import setup as setup_blueprint
app.register_blueprint(setup_blueprint)

@app.template_filter('timezone')
def convertTZ(time,clockFmt=12,Timezone="America/Anchorage"):
        dt_utc = time
        dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
        dt = dt_utc.astimezone(pytz.timezone(Timezone))
        if clockFmt == 12:
            outformat = "%-m/%-d/%y %-I:%M:%S %p"
        else:
            outformat = "%-m/%-d/%y %H:%M:%S"
        outTime = dt.strftime(outformat).lower()
        return outTime

# Setup mqtt_client
# Gather environment variables
ev_port = environ.get("MQTT_BROKER_PORT")
ev_topics = environ.get("MQTT_TOPICS")
ev_user = environ.get("MQTT_BROKER_USER")
ev_password = environ.get("MQTT_BROKER_PASSWORD")
ev_https = environ.get("MQTT_TRANSPORT")
ev_broker = environ.get("MQTT_BROKER")
ev_key = environ.get("MQTT_APIAUTH_KEY")
ev_url = environ.get('FEVR_URL')
ev_port = environ.get('FEVR_PORT')
ev_fevr = f"{ev_url}:{ev_port}"
ev_verbose = environ.get("MQTT_VERBOSE_LOGGING")

# Check to see if mqtt table exists.  If not, create the databse

if not inspect(db.engine).has_table("events"):
    db.create_all()
    MQTT = mqtt(port=ev_port,topics=ev_topics,user=ev_user,password=ev_password,https=ev_https,fevr=ev_fevr,broker=ev_broker,key=ev_key)
    db.session.add(MQTT)
    db.session.commit()
    
    
    
    
# Query the database
MQTT= mqtt.query.first()
command = f"/fevr/venv/bin/python /fevr/app/mqtt_client"
if MQTT.port != 1883:
    command += f" -p {MQTT.port}"
elif ev_port:
    command += f" -p {ev_port}"
    
if MQTT.topics != "frigate/+":
    command += f" -t {MQTT.topics}"
elif ev_topics:
    command += f" -t {ev_topics}"

if MQTT.user != "" and MQTT.password != "":
    command += f" -u {MQTT.user} -P {MQTT.password}"
if ev_user and ev_password:
    command += f" -u {ev_user}"
    command += f" -P {ev_password}"
    
    
if MQTT.https == "https":
    command += " -s "
if ev_https and ev_https == "https":
    command += f" -s"
    
if MQTT.fevr != "localhost:5090":
    command += f" -f {MQTT.fevr}"
if ev_url and ev_port:
    command += f" -f {ev_fevr}"
    
if ev_verbose and ev_verbose == "true":
    command += " -v"
    
if ev_broker:
    command += f" {ev_broker}"
else:
    command += f" {MQTT.broker}"

if ev_key:
    command +=f" {ev_key}"
else:
    command +=f" {MQTT.key}"
    
# Write new run_mqtt_client.sh:
with open('run_mqtt_client.sh', "w") as myfile:
    myfile.write(f"#!/bin/sh\n{command}")