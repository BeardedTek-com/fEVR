#!/usr/bin/python
class logit:
    def __init__(self,logfile="/var/www/logs/debug.log"):
        self.logfile = logfile
    def execute(self,msg,src='fEVR',level='debug',logpath='/var/www/logs'):
        from time import time
        self.logtime = "{:.4f}".format(time())
        self.logfile = f"{logpath}/{level}.log"
        logentry = f"{self.logtime} {str(msg)}\n"
        with open(self.logfile,"a+") as logFile:
            logFile.write(f"[ {src:15}] {logentry}")