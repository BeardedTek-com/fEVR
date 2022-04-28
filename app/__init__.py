# External Imports
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager
from datetime import timedelta
from datetime import datetime
from dateutil import tz
import pytz

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

from .models.models import User

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