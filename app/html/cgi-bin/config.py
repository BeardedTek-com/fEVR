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
class Config:
    def __init__(self,file='/var/www/config/config.json'):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.configFile = file
        self.reqdKeys = ['title','domain','admin','adminPassword','url','api','snap','clip']
        self.reqd = len(self.reqdKeys)
        self.exists = {}
        self.execute()
    def getConfig(self):
        from json import load
        with open(self.configFile) as configJSON:
            self.config = load(configJSON)
    def configCheck(self,count=0):
        for key in self.config:
            for value in key:
                for var in self.reqdKeys:
                    if var == value:
                        count += 1
        from os.path import exists
        if self.config['fevr']['debug'] == "true":
            self.config['debug'] = True
        else:
            self.config['debug'] = False
        
        self.debug = self.config['debug']
        self.exists['db'] = exists(self.config['fevr']['db'])
        if count == self.reqd and self.exists['db']:
            return True
    def execute(self):
        from os.path import exists
        if exists(self.configFile):
            self.getConfig()
            if exists(str(self.config['fevr']['db'])):
                return self.configCheck()
