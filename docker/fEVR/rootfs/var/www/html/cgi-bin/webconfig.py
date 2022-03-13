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
    def __init__(self,db="/var/www/data/db/fEVR.sqlite"):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.configDir = "/var/www/data/config"
        self.configFile = f"{self.configDir}/config.json"
        self.configBackup = f"{self.configDir}/backup/{round(time.time(),2)}.json"
        self.input = cgi.FieldStorage()
        self.error.execute(f"Processing Web Config...",src=self.script)
        self.db = db
        self.fatalError = False
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
        try:
            shutil.copyfile(self.configFile,self.configBackup)
            with open(self.configFile,"w+") as configFile:
                configFile.write(json.dumps(self.webconfig, indent=2,sort_keys=True))
        except:
            try:
                self.setPerms()
            except:
                self.fatal_error()
    def setPerms(self):
        errmsg = "\nCouldn't access the data directory.  Looks like the permissions are wonky."
        import os
        mode=0o770
        path="/var/www/data"
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chown(os.path.join(root,d),'100','101')
                os.chmod(os.path.join(root, d), mode)
                for f in files:
                    os.chown(os.path.join(root,f),'100','101')
                    os.chmod(os.path.join(root, f), mode)
        errmsg = "\nYou lucky dog.  fEVR took care of it for you!!!"
        self.error.execute(errmsg,self.script)
    def fatal_error(self):
        from os import environ
        imgName=environ.get('FEVR_CONTAINER_NAME',"fevr")
        errmsg =  f"\n\
                    ############################### FATAL ERROR 64617461207065726D73 ################################\n\
                    Whoops!  fEVR can't take care of this one for you.\n\
                    Please run the following command:\n\
                    docker-compose exec {imgName} chown -R 100:101 /var/www/data && chmod -R 0770 /var/www/data\n\
                    #################################################################################################"
        public_errmsg ="\n\
                    ############################### FATAL ERROR 64617461207065726D73 ################################\n\
                    \n\
                                       Please contact your site admin and give him this code.\n\
                    \n\
                    #################################################################################################"
        print('content-type: text/plain\n\n')
        print(public_errmsg)
        self.error.execute(errmsg,self.script)
        self.fatalError=True
    def dbSetup(self):
        dbTooSmall = False
        dbPathExists = False
        db = self.webconfig['fevr']['db']
        if exists(db):
            dbPathExists = True
            if getsize(db) < 24576:
                dbTooSmall = True
        if not dbPathExists or dbTooSmall:
            try:
                from shutil import copy
                copy(self.db,db)
            except:
                self.fatal_error()

    def execute(self):
        self.webConfig()
        self.writeConfig()
        self.dbSetup()
        if not self.fatalError:
            print('content-type: text/html\n\n')
            print("<script>parent.location='../'</script>")
def main():

    wconfig = webConfig()
    wconfig.execute()
main()
