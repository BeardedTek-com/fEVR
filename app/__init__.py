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
# Gather environment variables in a dict
ev = {}
ev["port"] = environ.get("MQTT_BROKER_PORT")
ev["MQTT_TOPICS"] = environ.get("MQTT_TOPICS")
ev["MQTT_BROKER_USER"] = environ.get("MQTT_BROKER_USER")
ev["MQTT_BROKER_PASSWORD"] = environ.get("MQTT_BROKER_PASSWORD")
ev["MQTT_TRANSPORT"] = environ.get("MQTT_TRANSPORT")
ev["MQTT_BROKER"] = environ.get("MQTT_BROKER")
ev["MQTT_APIAUTH_KEY"] = environ.get("MQTT_APIAUTH_KEY")
ev["FEVR_URL"] = environ.get('FEVR_URL')
ev["FEVR_PORT"] = environ.get('FEVR_PORT')
ev["fevr"] = f"{ev['url']}:{ev['port']}"
ev["MQTT_VERBOSE_LOGGING"] = environ.get("MQTT_VERBOSE_LOGGING")

def create_mqtt_entry(db,ev):
    port = 1883 if not ev["MQTT_BROKER_PORT"] else ev["MQTT_BROKER_PORT"]
    topics = "frigate/+" if not ev["MQTT_TOPICS"] else ev["MQTT_TOPICS"]
    user = "" if not ev["MQTT_BROKER_USER"] else ev["MQTT_BROKER_USER"]
    password = "" if not ev["MQTT_BROKER_PASSWORD"] else ev["MQTT_BROKER_PASSWORD"]
    https = "http" if not ev["MQTT_TRANSPORT"] else ev["MQTT_TRANSPORT"]
    broker = "mqtt" if not ev["MQTT_BROKER"] else ev["MQTT_BROKER"]
    key = "" if not ev["MQTT_APIAUTH_KEY"] else ev["MQTT_APIAUTH_KEY"]
    url = "fevr" if not ev["FEVR_URL"] else ev["FEVR_URL"]
    FEVR_PORT = "5090" if not ev["FEVR_PORT"] else ev["FEVR_PORT"]
    fevr = f"{url}:{FEVR_PORT}"

    MQTT = mqtt(port=port,topics=topics,user=user,
                password=password,https=https,
                fevr=fevr,broker=broker,key=key)
    db.session.add(MQTT)
    db.session.commit()


# Check to see if mqtt table exists.  If not, create the databse and create a default entry
if not inspect(db.engine).has_table("mqtt"):
    db.create_all()
    create_mqtt_entry(db,ev)
# Query the mqtt table and if MQTT=None, create an entry
MQTT= mqtt.query.first()
if not MQTT:
    create_mqtt_entry(db,ev)
    
    
MQTT= mqtt.query.first()
command = f"/fevr/venv/bin/python /fevr/app/mqtt_client"
if MQTT.port != 1883:
    command += f" -p {MQTT.port}"
if MQTT.topics != "frigate/+":
    command += f" -t {MQTT.topics}"
if MQTT.user != "" and MQTT.password != "":
    command += f" -u {MQTT.user} -P {MQTT.password}" 
if MQTT.https == "https":
    command += " -s "
if MQTT.fevr != "localhost:5090":
    command += f" -f {MQTT.fevr}"
if ev["MQTT_VERBOSE_LOGGING"] and ev["MQTT_VERBOSE_LOGGING"] == "true":
    command += " -v"
if MQTT.broker != "mqtt":
    command += f" {MQTT.broker}"

if MQTT.key:
    command +=f" {MQTT.key}"
else:
    command +=" key"
    
# Write new run_mqtt_client.sh:
with open('run_mqtt_client.sh', "w") as myfile:
    myfile.write(f"#!/bin/sh\n{command}")