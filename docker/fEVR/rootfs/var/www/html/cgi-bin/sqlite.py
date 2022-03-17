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
import sqlite3
from sqlite3 import Error
class sqlite:
    def __init__(self,debug=False,db="/var/www/data/db/fEVR.sqlite"):
        self.db = db
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.conn = None
        self.version = ""
        self.debug = debug
        self.fatalerror =  f"\n\
        ############################### FATAL ERROR ###############################\n\
        \n\
        ##MESSAGE##\
        \n\
        ###########################################################################"
    def open(self):
        try:
            if self.debug:
                self.error.execute(f"connecting to {self.db}.....\n",src=self.script)
            self.conn = sqlite3.connect(self.db)
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
    def count(self,sql):
        e = ""
        try:
            exe = self.conn.execute(sql)
            cnt = exe.fetchone()
            return cnt[0]
        except Error as e:
            return f"ERROR: {str(e).split(':')}"
        finally:
            self.close()

    def retrieve(self,sql,count=0):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql)
                records = cursor.fetchall()
                cursor.close
                return records
            except:
                self.error.execute(f"No results returned from {self.db}", self.script)
                return []
        except:
            msg =f"Permissions improperly set on {self.db}"
            try:
                import subprocess
                data = subprocess.check_output("/opt/fevr/setup/dbsetperms '/var/www/data/db'", shell=True)
                self.error.exeture(data,self.script)
            except:
                from os import environ
                imgName=environ.get('FEVR_CONTAINER_NAME',"fevr")
                msg += f"\n Cannot automatically set permissions. Please run the following command on your host:\n\
                         docker exec -it {imgName} chown -R 100:101 /var/www/data && chmod -R 0770 /var/www/data"
            finally:
                errmsg = self.fatalerror.replace("##MESSAGE##",msg)

            self.error.execute(errmsg, self.script)
        