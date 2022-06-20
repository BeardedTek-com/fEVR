# External Imports
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
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
MQTT= mqtt.query.first()
command = f"/fevr/venv/bin/python /fevr/app/mqtt_client"
if MQTT.port != 1883:
    command += f" -p {MQTT.port}"
elif environ.get("MQTT_BROKER_PORT"):
    command += f" -p {environ.get('MQTT_BROKER_PORT')}"
    
if MQTT.topics != "frigate/+":
    command += f" -t {MQTT.topics}"
elif environ.get("MQTT_TOPICS"):
    command += f" -p {environ.get('MQTT_TOPICS')}"

if MQTT.user != "" and MQTT.password != "":
    command += f" -u {MQTT.user} -P {MQTT.password}"
if environ.get("MQTT_BROKER_USER") and environ.get("MQTT_BROKER_PASSWORD"):
    command += f" -u {environ.get('MQTT_BROKER_USER')}"
    command += f" -P {environ.get('MQTT_BROKER_PASSWORD')}"
    
    
if MQTT.https == "https":
    command += " -s "
if environ.get("FEVR_TRANSPORT") and environ.get("FEVR_TRANSPORT") == "true":
    command += f" -s"
    
if MQTT.fevr != "localhost:5090":
    command += f" -f {MQTT.fevr}"
if environ.get("FEVR_URL") and environ.get("FEVR_PORT"):
    command += f" -f {environ.get('FEVR_URL')}:{environ.get('FEVR_PORT')}"
    
if environ.get("MQTT_VERBOSE_LOGGING"):
    command += " -v"
    
if environ.get("MQTT_BROKER"):
    command += f" {environ.get('MQTT_BROKER')}"
else:
    command += f" {MQTT.broker}"

if environ.get("MQTT_APIAUTH_KEY"):
    command +=f" {environ.get('MQTT_APIAUTH_KEY')}"
else:
    command +=f" {MQTT.key}"
    
# Write new run_mqtt_client.sh:
with open('run_mqtt_client.sh', "w") as myfile:
    myfile.write(f"#!/bin/sh\n{command}")