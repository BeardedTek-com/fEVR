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