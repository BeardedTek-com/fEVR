#!/usr/bin/python
import cgi
import json
import shutil
import time
class webConfig:
    def __init__(self):
        self.configDir = "/var/www/config"
        self.configFile = f"{self.configDir}/config.json"
        self.configBackup = f"{self.configDir}/backup/{time.time()}.json"
        self.input = cgi.FieldStorage()
        print('content-type: text/html\n\n')
    def webConfig(self):
        import cgi
        self.input = cgi.FieldStorage()
        self.webconfig = {}
        self.webconfig['fevr'] = {}
        self.webconfig['frigate'] = {}
        for var in ('title', 'base','html','db','debug'):
            self.webconfig['fevr'][var] = self.input.getvalue(var)
        for var in ('url','apiEventPath','snapPath','clipPath'):
            self.webconfig['frigate'][var] = self.input.getvalue(var)
    def toJSON(self):
        return json.dumps(self.webconfig, indent=2,sort_keys=True)
    def writeConfig(self):
        
        shutil.copyfile(self.configFile,self.configBackup)
        with open(self.configFile,"w+") as configFile:
            configFile.write(self.toJSON())
    def execute(self):
        self.webConfig()
        self.writeConfig()
        print("<script>parent.location.reload()</script>")
def main():
    wconfig = webConfig()
    wconfig.execute()

main()
