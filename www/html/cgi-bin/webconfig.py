#!/usr/bin/python
import cgi
import json
import shutil
import time
from os.path import exists
class webConfig:
    def __init__(self):
        from os.path import basename
        self.script = basename(__file__)
        from logging import logging as flogging
        self.error = flogging()
        self.configDir = "/var/www/config"
        self.configFile = f"{self.configDir}/config.json"
        self.configBackup = f"{self.configDir}/backup/{time.time()}.json"
        self.input = cgi.FieldStorage()
        self.error.execute(f"Processing Web Config...",src=self.script)
        print('content-type: text/html\n\n')
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
            self.webconfig['frigate'][var] = self.input.getvalue(var)
        self.error.execute(f"{self.webConfig}",src=self.script)
    def toJSON(self):
        return json.dumps(self.webconfig, indent=2,sort_keys=True)
    def writeConfig(self):
        shutil.copyfile(self.configFile,self.configBackup)
        with open(self.configFile,"w+") as configFile:
            configFile.write(self.toJSON())
    def dbSetup(self):
        if not exists(self.webconfig['fevr']['db']):
            blankDB = f"{self.webconfig['fevr']['base']}/db/fEVR.blank.sqlite"
            shutil.copyfile(blankDB,self.webconfig['fevr']['db'])
            self.error.execute(f"Copying {blankDB} to {self.webconfig['fevr']['db']}",src=self.script)
    def execute(self):
        self.webConfig()
        self.writeConfig()
        self.dbSetup()
        print("<script>parent.location.reload()</script>")
def main():

    wconfig = webConfig()
    wconfig.execute()
main()
