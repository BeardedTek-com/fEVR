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
class event:
    def __init__(self,frigate,fevr,stub='/var/www/html/stub/eventdetail.html',db='/var/www/data/db/fEVR.sqlite'):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.frigate = frigate
        self.fevr = fevr
        import cgi
        self.input = cgi.FieldStorage()
        self.error.execute(f"self.input: {self.input}",self.script)
        self.id = self.input.getvalue('id')
        self.action = self.input.getvalue('action')
        self.stub = stub
        self.db = db
        self.event = self.getEvent()
        self.referrer = ""
    def convertTZ(self,dt_str):
        from datetime import datetime
        from dateutil import tz
        import pytz
        format = "%Y-%m-%d %H:%M:%S"
        dt_utc = datetime.strptime(dt_str,format)
        dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
        return dt_utc.astimezone(pytz.timezone('America/Anchorage'))
    def getEvent(self):
        from sqlite import sqlite
        SQL = f"""SELECT * FROM events WHERE event='{self.id}' ORDER BY event DESC LIMIT 1"""
        self.error.execute(SQL,src=self.script)
        hpsql = sqlite(db=self.db)
        hpsql.open()
        items = hpsql.retrieve(SQL)
        for row in items:
            event={}
            event['id'] = row[1]
            event['camera'] = row[2]
            event['type'] = row[3]
            event['ack'] = row[4]
            event['clip'] = row[5]
            event['snap'] = row[6]
            event['score'] = row[7]
        return event
    def delEvent(self):
        if self.action == "delEvent":
            from fetch import fetchEvent
            fetch = fetchEvent(self.frigate,self.id)
            fetch.delEvent()
            self.referrer = self.input.getvalue('referrer')
            self.error.execute(f"self.referrer: {self.referrer}",src=self.script)
            data = True
        else:
            data = False
        return data
    def displayEvent(self):
        from fetch import fetchEvent
        fetch = fetchEvent(self.frigate,self.id)
        import os
        from datetime import datetime
        time = datetime.fromtimestamp(int(self.id.split('.')[0]))
        ftime = str(self.convertTZ(str(time))).rsplit('-')
        self.event['time'] = f"{ftime[0]}-{ftime[1]}-{ftime[2]}"
        if self.event['ack'] == "true":
            newClass = "newhidden"
            ackAction = "Unacknowledge"
            ackLink = f"?id={self.id}&action=unack"
        else:
            newClass= ""
            ackAction = "Acknowledge"
            ackLink = f"?id={self.id}&action=ack"
        refreshLink = f"?id={self.id}&action=refreshEvent"
        delLink = f"?id={self.id}&action=delEvent"
        if os.path.isfile(self.stub):
            with open(self.stub) as eventStub:
                thumbURL = f"../events/{self.id}/thumb.jpg"
                data = eventStub.read()
                if self.action == "clip" and self.event['clip'] != "no":
                    view = f"<video class='clip' controls autoplay>\n<source src='../events/##EVENT##/clip.mp4' type='video/mp4'>\n</video>"
                elif self.action == "snap" and self.event['snap'] != "no":
                    view = f"<img class='snap' src='../events/##EVENT##/snapshot.jpg'/>\n"
                elif self.action == "live":
                    view = f"<iframe class='live' src='##FRIGATE##/api/##CAMERA##'></iframe>"
                elif self.action == "refreshEvent":
                    from fetch import fetchEvent
                    fetch = fetchEvent(self.frigate,self.id)
                    fetch.delEvent(db=False)
                    fetch.getEvent()
                    view = f"<script>location.href='?id={self.id}';</script>"
                elif self.action == "ack":
                    from fetch import fetchEvent
                    fetch = fetchEvent(self.frigate,self.id)
                    fetch.ackEvent('true')
                    view = f"<script>location.href='?id={self.id}';</script>"
                elif self.action == "unack":
                    from fetch import fetchEvent
                    fetch = fetchEvent(self.frigate,self.id)
                    fetch.ackEvent('')
                    view = f"<script>location.href='?id={self.id}';</script>"
                else:
                    view = ""
                data = data.replace("##VIEW##",view)
                data = data.replace("##NEWCLASS##",newClass)
                data = data.replace("##ACK##",ackLink)
                data = data.replace("##ACKACTION##",ackAction)
                data = data.replace("##DEL##",delLink)
                data = data.replace("##REFRESH##",refreshLink)
                data = data.replace('##THUMB##',thumbURL)
                data = data.replace("##TIME##",str(self.event['time']))
                data = data.replace("##EVENT##",self.id)
                data = data.replace("##TYPE##",self.event['type'])
                data = data.replace("##CAMERA##",self.event['camera'])
                data = data.replace("##TTYPE##",self.event['type'].capitalize())
                data = data.replace("##TCAMERA##",self.event['camera'].capitalize())
                data = data.replace("##FRIGATE##",self.frigate['url'])
        return data
                
def main():
    from config import Config
    myConfig = Config()
    print('content-type: text/html; charset=UTF-8\n\n')
    hpf = event(myConfig.config['frigate'],myConfig.config['fevr'])
    if hpf.delEvent():
        from time import sleep
        sleep(0.25)
        print(f"<script>location.href='{hpf.referrer}'</script>")
    else:
        print(hpf.displayEvent())
main()