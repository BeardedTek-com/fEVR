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
        self.conn = None
        self.error = ""
        self.version = ""
        self.debug = debug

    def open(self,db="default.sqlite"):
        try:
            if self.debug:
                print(f"connecting to {db}.....\n")
            self.conn = sqlite3.connect(db)
        except Error as e:
            self.error = e
            if self.debug:
                print(f"Gathered Error Message: {self.error}\n")

    def close(self):
        if self.debug:
            print("Is the connecion open?\n")
        if self.conn:
            if self.debug:
                print("yes.  yes it is.\n")
            self.conn.commit()
            if self.debug:
                print("committing")
            self.conn.close()
            if self.debug:
                print("closed.\n")
    
    def execute(self,sql):
        retval = []
        e = ""
        try:
            exe = self.conn.execute(sql)
            if self.debug:
                print(f"Executed SQL: {sql}")
            retval = [0,sql,exe]
        except Error as e:
            retval = [1,sql,str(e).split(":")]
        finally:
            self.close()
            print(retval)
            return retval
    
    def retrieve(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close
        return records