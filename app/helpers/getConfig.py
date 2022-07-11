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

import yaml
from os import path, access, R_OK
from app.helpers.logit import logit
from app import configFile
def getConfig(self,config):
        if path.isfile(config) and access(config, R_OK):
            with open(config) as configFile:
                try:
                    Config = yaml.safe_load(configFile)
                except Exception as e:
                    logit.execute(f"ERROR: {e}",src=self.script)
                    Config = {}
                values = ['fevr_host','fevr_port','fevr_transport','mqtt_apikey','mqtt_broker','mqtt_port','mqtt_user','mqtt_password','mqtt_topics','verbose']
                for value in values:
                    try:
                        # Check if value exists
                        test = Config[value]
                    except KeyError:
                        # If not, set it to None
                        Config[value] = None
            Config["error"] = None
        else:
            if path.isfile(config):
                Config["error"] = "File not readable"
            Config["error"] = "File does not exist"
        return Config

if __name__ == "__main__":
    print(getConfig(configFile))