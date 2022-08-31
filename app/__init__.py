#    This code is a portion of frigate Event Video Recorder (fEVR)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# External Imports
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager
from datetime import timedelta
import pytz
from app.helpers.convert import convert

# Config File
configFile = "data/config"

# Flask app Setup
app = Flask(__name__)
app.config.from_file('config.json',load=json.load)



# Setup Session Timeout
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Database Setup
db = SQLAlchemy(app)
app.SQLALCHEMY_TRACK_MODIFICATIONS=False

from app.models.user import User

# Flask Login Setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import Blueprints
from app.blueprints.api import api as api_blueprint
app.register_blueprint(api_blueprint)

from app.blueprints.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.blueprints.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from app.blueprints.setup import setup as setup_blueprint
app.register_blueprint(setup_blueprint)


# Define Templates
@app.template_filter('timezone')
def convertTZ(time,clockFmt=12,Timezone="America/Anchorage"):
        convert.convertTZ(time,clockFmt,Timezone)