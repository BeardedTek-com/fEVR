#!/usr/bin/python
#    fEVR (Frigate Event Video Recorder) RESTful Interface
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
import json

import sys
class rest:
    def __init__(self,frigate):
        self.sql = ""
        self.debug = ""
        self.frigate = frigate
    def error(self,msg,level='debug',logpath='/var/www/logs'):
        logfile = f"{logpath}/{level}.log"
        from time import time
        from os.path import basename
        script = basename(__file__)
        logentry = f"{time()} {str(msg)}\n"
        with open(logfile,"a+") as logFile:
            logFile.write(f"[{script}]{logentry}")
    def load_json(self,src="POST",file=None):
        if src == 'POST':
            self.input = json.loads(sys.stdin.read())
            sys.stderr.write(f"{str(self.input)}")
            self.error_log("RECEIVED\n")
            self.error_log(str(self.input))
        elif src == 'FILE':
            with open(file) as page_json:
                self.input = json.load(page_json)        
    def parse_json(self):
        self.fields = []
        self.values = []
        self.function = ""
        self.create = []
        if self.input['debug'] == "1" or "true" or "yes":
            self.debug = True
        else:
            self.debug = False
        self.table = self.input['table']
        self.function = self.input['function']
        if self.input['columns']['event']:
            self.id = self.input['columns']['event']
        for index in self.input['columns']:
            self.fields.append(index)
            value = self.input['columns'][index]
            self.values.append(value)
            if self.function == "CREATE":
                self.create.append([index,value])
        self.error_log(f"table: {self.table}")
        self.error_log(f"function: {self.function}")
        self.error_log(f"fields: {self.fields}")
        self.error_log(f"values: {self.values}")
        return True
    def json2sql(self):
        if self.function == "CREATE":
            # CREATE TABLE IF NOT EXISTS events(id integer PRIMARY KEY,
            # event_id text UNIQUE, camera text, bbox text, ack text);
            SQL = f"""CREATE TABLE IF NOT EXISTS {self.table}("""
            for field in self.create:
                if field == self.create[-1]:
                    SQL += f"""{field[0]} {field[1]});"""
                else:
                    SQL += f"""{field[0]} {field[1]},"""
            return SQL
        if self.function == "SELECT":
            # SELECT <{index}>, <{index}>, <{index}>, id from <{input['table']}>
            SQL = """SELECT """
            for field in self.fields:
                if field == self.fields[-1]:
                    SQL += f"""{field} from {self.table}"""
                else:
                    SQL += f"""{field},"""
            return SQL
        elif self.function == "INSERT":
            # INSERT INTO <table> ({index},{index},{index},id) \
            # VALUES ({value}, {value}, {value}, null)
            SQL = f"""INSERT INTO {self.table}("""
            for field in self.fields:
                if field == self.fields[-1]:
                    SQL += f"""{field}) VALUES("""
                else:
                    SQL += f"""{field},"""
            for value in self.values:
                if value == self.values[-1]:
                    SQL += f"""'{value}')"""
                else:
                    SQL += f"""'{value}',"""
            return SQL
    def loadEvent(self):
        from fetch import fetchEvent
        fetch = fetchEvent(self.frigate,self.id)
        fetch.getEvent()
    def deleteEvent(self):
        from fetch import fetchEvent
        fetch = fetchEvent(self.frigate,self.id)
        fetch.delEvent()

def main():
    from config import Config
    myConfig = Config()
    myConfig.getConfig()
    from sqlite import sqlite
    fRest=rest(myConfig.config['frigate'])
    # Print headers in case we're talking to a web browser...
    print("content-type: text/plain\n\n")
    fRest.load_json()
    fRest.parse_json()
    isEvent = fRest.loadEvent()
    if isEvent != 20:
        sql = fRest.json2sql()
        fRest.error_log(sql)
        hpsql = sqlite()
        hpsql.open("/var/www/db/fEVR.sqlite")
        if hpsql.error:
            fRest.error_log(f"Error: {hpsql.error}")
        else:
            temp = hpsql.execute(sql)
            fRest.error_log(temp)
        fRest.error_log("OK")
    else:
        fRest.error_log("Not a valid Frigate Event")
        fRest.deleteEvent()
        sql = 

main()
