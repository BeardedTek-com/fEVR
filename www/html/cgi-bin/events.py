#!/usr/bin/python
#    fEVR (Frigate Event Video Recorder) Events Menu
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
import os
stub='../stub/event.html'
class events:
    def __init__(self):
        self.getOptions()
    def getOptions(self):
        import cgi
        fieldStorage = cgi.FieldStorage()
        self.count=""
        self.order=""
        self.selectors={}
        self.extraOptions={}
        for key in fieldStorage.keys():
            item = fieldStorage.getvalue(key)
            if key == 'count':
                self.count = item
            elif key == 'order':
                self.order = item
            else:
                for field in ['camera','type','ack','clip','snap','score']:
                    if key == field:
                        self.selectors[key] = item
                    else:
                        self.extraOptions[key] = item
    def error(self,msg,level='debug'):
        if self.debug or level == 'info':
            from sys import stderr
            stderr.write(f"{str(msg)}\n")
    def getEvent(self,event,thumbSize=180,location='/var/www/html/events/'):
        eventPATH = f"{location}{event['id']}"
        snapPATH = f"{eventPATH}{self.frigate['snap']}"
        thumbPATH= f"{eventPATH}/thumb.jpg"
        clipPATH = f"{location}{event['id']}{self.frigate['clip']}"
        if not os.path.exists(thumbPATH):
            if not os.path.exists(eventPATH):
                os.makedirs(eventPATH)
            snapURL = f"{self.frigate['url']}{self.frigate['api']}{event['id']}{self.frigate['snap']}"
            clipURL = f"{self.frigate['url']}{self.frigate['api']}{event['id']}{self.frigate['clip']}"
            import requests
            snap = requests.get(snapURL, allow_redirects=True)
            open(snapPATH,'wb').write(snap.content)
            self.resizeImg(snapPATH,thumbPATH,thumbSize)
            clip = requests.get(clipURL, allow_redirects=True)
            open(clipPATH,'wb').write(clip.content)
    def resizeImg(self,img,thumbPATH,height=180,ratio=(16/9)):
        # Resizes an image from the filesystem
        size = (int((height*ratio)),height)
        from PIL import Image as CompressImage
        picture = CompressImage.open(img)
        thumb = picture.resize(size)
        thumb.save(thumbPATH,"JPEG",optimize=True)
    def convertTZ(self,dt_str):
        from datetime import datetime
        from dateutil import tz
        import pytz
        format = "%Y-%m-%d %H:%M:%S"
        dt_utc = datetime.strptime(dt_str,format)
        dt_utc = dt_utc.replace(tzinfo=pytz.UTC)
        return dt_utc.astimezone(pytz.timezone('America/Anchorage'))

    def generateEventDiv(self,event):
        from datetime import datetime
        time = datetime.fromtimestamp(int(event['id'].split('.')[0]))
        ftime = str(self.convertTZ(str(time)))
        event['time'] = ftime[ftime.index('-')+1:]
        if os.path.isfile(stub):
            with open(stub) as eventStub:
                url = f"/cgi-bin/event.py?id={event['id']}"
                thumbURL = f"/events/{event['id']}/thumb.jpg"
                caption = f"{event['time']}<br/>\n {event['type']} detected in {event['camera']}"
                data = eventStub.read()
                data = data.replace('##EVENT_URL##',url)
                data = data.replace('##EVENT_IMG##',thumbURL)
                data = data.replace('##EVENT_CAPTION##',caption)
        if data:
            return data
    def getStub(self,stub):
        if os.path.isfile(stub):
            with open(stub) as Stub:
                return Stub.read()
    def getEvents(self,count=False,selectors=False,order=False):
        wheres = ""
        if selectors:
            for key in selectors:
                self.error(selectors[key])
                self.error(f"COUNT: {count}")
                wheres += f"""WHERE {key}='{selectors[key]}'"""
        sql = """SELECT * FROM events """
        if wheres:
            sql += wheres
        if order:
            if order['field'] and order['direction']:
                sql += f"""ORDER BY {order['field']} {order['direction']}"""
        else:
            sql += """ORDER BY event DESC"""
        if count:
            count = int(count)
            
        from fetch import fetchEvent
        from sqlite import sqlite
        fsqlite = sqlite()
        fsqlite.open(self.fevr['db'])
        self.error(sql)
        items = fsqlite.retrieve(sql)
        n = 1
        data =""
        for row in items:
            event = {}
            event['id'] = row[1]
            event['camera'] = row[2]
            event['type'] = row[3]
            event['ack'] = row[4]
            event['clip'] = row[5]
            event['snap'] = row[6]
            event['score'] = row[7]
            fetchevent = fetchEvent(self.frigate,event['id'])
            fetchevent.execute()
            data += self.generateEventDiv(event)
            if count:

                if count != 0:
                    n += 1
                    if n > count:
                        break
        if n <= 1:
            print('No Results...  Are you sure you configured everything right? <a href="/install.html">Config</a>')
        return data
    def execute(self):
        from config import Config
        fconfig = Config()
        print('content-type: text/html; charset=UTF-8\n\n')
        print()
        if fconfig.exists:
            self.debug = fconfig.debug
            self.config = fconfig.config
            self.frigate = self.config['frigate']
            self.fevr = self.config['fevr']
            self.error(self.frigate)
            self.error(self.fevr)
            header = self.getStub(f"/var/www/html/stub/eventsHeader.html")
            content = self.getEvents(self.count,self.selectors,self.order)
            footer = self.getStub(f"{self.fevr['html']}/stub/eventsFooter.html")
        else:
            header = self.getStub("/var/www/html/stub/eventsHeader.html")
            content = self.getStub("/var/www/html/install.html")
            footer = self.getStub("/var/www/html/stub/eventsFooter.html")
        print(f"{header}{content}{footer}")

def main():
    fevents = events()
    fevents.execute()
main()