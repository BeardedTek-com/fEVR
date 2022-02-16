#!/usr/bin/python
class Config:
    def __init__(self):
        self.reqdKeys = ['title','domain','admin','adminPassword','url','api','snap','clip']
        self.reqd = len(self.reqdKeys)
        self.getConfig()
        if self.exists:
            if self.configCheck(self.config):
                return True
    def getConfig(self,file='/var/www/config/config.json'):
        import json
        from os.path import exists
        self.exists = exists(file)
        if self.exists:
            with open(file) as configJSON:
                self.config = json.load(configJSON)
    def configCheck(self,config,count=0):
        for key in config:
            for value in key:
                for var in self.reqdKeys:
                    if var == value:
                        count += 1
        if count == self.reqd:
            return True
            
