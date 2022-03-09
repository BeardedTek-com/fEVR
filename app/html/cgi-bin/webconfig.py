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
import cgi
import json
import shutil
import time
from os.path import exists
from os.path import getsize
class webConfig:
    def __init__(self):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.configDir = "/var/www/config"
        self.configFile = f"{self.configDir}/config.json"
        self.configBackup = f"{self.configDir}/backup/{round(time.time(),2)}.json"
        self.input = cgi.FieldStorage()
        self.error.execute(f"Processing Web Config...",src=self.script)
    def webConfig(self):
        import cgi
        self.input = cgi.FieldStorage()
        self.error.execute(f"{self.input}",src=self.script)
        self.webconfig = {}
        self.webconfig['fevr'] = {}
        self.webconfig['frigate'] = {}
        for var in ('title', 'base','html','db','debug'):
            self.webconfig['fevr'][var] = self.input.getvalue(var)
        for var in ('url','apiEventPath','snapPath','clipPath'):
            self.webconfig['frigate'][var] = str(self.input.getvalue(var))
        self.error.execute(f"New Config.json:\n{str(self.webconfig)}",src=self.script)
    def writeConfig(self):
        shutil.copyfile(self.configFile,self.configBackup)
        with open(self.configFile,"w+") as configFile:
            configFile.write(json.dump(self.webconfig, indent=2,sort_keys=True))
    def dbSetup(self):
        db = self.webconfig['fevr']['db']
        if exists(db):
            dbPathExists = True
            if getsize(db) < 24576:
                dbTooSmall = True
        if not dbPathExists or dbTooSmall:
            from shutil import copy
            from os import chown
            copy("/var/www/default/fEVR.sqlite",db)
            chown(db,100,101)

    def execute(self):
        self.webConfig()
        self.writeConfig()
        self.dbSetup()
        print('content-type: text/html\n\n')
        print("<script>parent.location='../'</script>")
def main():

    wconfig = webConfig()
    wconfig.execute()
main()
