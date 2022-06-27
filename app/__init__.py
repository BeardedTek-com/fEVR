# External Imports
from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy, inspect
from sqlalchemy import desc
import json
from flask_login import LoginManager
from datetime import timedelta
from datetime import datetime
from dateutil import tz
import pytz
from os import environ,path,access,R_OK

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
# NOTE: Environment Variables are only used if app/data/config.json does not exist.

def writeConfigFile(file,ev):
    config = {}
    config["fevr_url"] = f"{ev['FEVR_URL']}:{ev['FEVR_PORT']"
    config["fevr_transport"] = ev["MQTT_TRANSPORT"]
    config["fevr_apikey"] = ev["MQTT_APIAUTH_KEY"]
    config["mqtt_broker"] = ev["MQTT_BROKER"]
    config["mqtt_port"] = ev["MQTT_BROKER_PORT"]
    config["mqtt_user"] = ev["MQTT_BROKER_USER"]
    config["mqtt_password"] = ev["MQTT_BROKER_PASSWORD"]
    config["mqtt_topics"] = ev["MQTT_TOPICS"]
    config["verbose"] = ev["MQTT_VERBOSE_LOGGING"]
    with open('/fevr/app/data/config.json', "w") as configFile:
        json.dump(config,configFile,sort_keys=True,indent=0)

ev = {}
ev["MQTT_BROKER_PORT"] = environ.get("MQTT_BROKER_PORT")
ev["MQTT_TOPICS"] = environ.get("MQTT_TOPICS")
ev["MQTT_BROKER_USER"] = environ.get("MQTT_BROKER_USER")
ev["MQTT_BROKER_PASSWORD"] = environ.get("MQTT_BROKER_PASSWORD")
ev["MQTT_TRANSPORT"] = environ.get("MQTT_TRANSPORT")
ev["MQTT_BROKER"] = environ.get("MQTT_BROKER")
ev["MQTT_APIAUTH_KEY"] = environ.get("MQTT_APIAUTH_KEY")
ev["FEVR_URL"] = environ.get('FEVR_URL')
ev["FEVR_PORT"] = environ.get('FEVR_PORT')
ev["MQTT_VERBOSE_LOGGING"] = environ.get("MQTT_VERBOSE_LOGGING")

config="/fevr/app/data/config.json"
if not path.isfile(config) or not access(config, R_OK):
    writeConfigFile(config,ev)