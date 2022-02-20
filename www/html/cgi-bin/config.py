#!/usr/bin/python
class Config:
    def __init__(self,file='/var/www/config/config.json'):
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