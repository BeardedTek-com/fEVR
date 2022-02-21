#!/usr/bin/python
#    fEVR (Frigate Event Video Recorder) SQLite Interface
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
import sqlite3
from sqlite3 import Error
class sqlite:
    def __init__(self,debug=False):
        from os.path import basename
        self.script = basename(__file__)
        from logging import logging as flogging
        self.error = flogging()
        self.conn = None
        self.version = ""
        self.debug = debug
    def open(self,db="/var/www/db/fEVR.sqlite"):
        try:
            if self.debug:
                self.error.execute(f"connecting to {db}.....\n",src=self.script)
            self.conn = sqlite3.connect(db)
        except Error as e:
            if self.debug:
                self.error.execute(e,src=self.script)
    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.error.execute('SQL Connection Closed',src=self.script)
    def execute(self,sql):
        retval = []
        e = ""
        try:
            exe = self.conn.execute(sql)
            if self.debug:
                self.error.execute(f"Executed SQL: {sql}",src=self.script)
            retval = [0,sql,exe]
        except Error as e:
            retval = [1,sql,str(e).split(":")]
        finally:
            self.close()
            self.error.execute(retval,src=self.script)
            return retval
    
    def retrieve(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close
        return records