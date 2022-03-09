#!/usr/bin/python
#    fEVR (frigate Event Video Recorder)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
class frigateConfig:
    def __init__(self,frigateURL):
        self.error = False
        self.url = frigateURL
        self.configAPI = "/api/config"
        self.cameras = {}
        self.getConfig()
        self.getCameras()
    def getConfig(self):
        try:
            configURL = f"{self.url}{self.configAPI}"
            import requests
            frigateConfig = requests.get(configURL, allow_redirects=True)
            import json
            self.frigateConfig = json.loads(frigateConfig.content)
        except:
            self.error = True
    def getCameras(self):
        for camera in self.frigateConfig['cameras']:
            self.cameras[camera] = {}
            self.cameras[camera]['objects'] = []
            for object in self.frigateConfig['cameras'][camera]['record']['events']['objects']:
                self.cameras[camera]['objects'].append(object)
