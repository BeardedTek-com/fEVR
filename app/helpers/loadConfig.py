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

def load_config(config_file):
    with open(config_file, "r") as config_fh:
        config = config_fh.read()
    myConfig = {}
    try:
        myConfig = yaml.safe_load(config)
    except:
        myConfig = {}
    return myConfig

if __name__ == "__main__":
    print(load_config("/home/localadmin/Documents/GitHub/fEVR/app/data/config.yml.template"))