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
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.sql = ""
        self.debug = ""
        self.frigate = frigate
    def load_json(self,src="POST",file=None):
        if src == 'POST':
            self.input = json.loads(sys.stdin.read())
            sys.stderr.write(f"{str(self.input)}")
            self.error.execute("RECEIVED\n",src=self.script)
            self.error.execute(str(self.input),src=self.script)
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
        self.error.execute(f"table: {self.table}",src=self.script)
        self.error.execute(f"function: {self.function}",src=self.script)
        self.error.execute(f"fields: {self.fields}",src=self.script)
        self.error.execute(f"values: {self.values}",src=self.script)
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
        fRest.error(sql)
        hpsql = sqlite()
        hpsql.open("/var/www/db/fEVR.sqlite")
        fRest.error(hpsql.execute(sql))
    else:
        fRest.error("Not a valid Frigate Event")
        fRest.deleteEvent()
main()