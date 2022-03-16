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
import os
stub='../stub/event.html'
class events:
    def __init__(self):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.getOptions()
        self.noResults = False
        self.getFilterValues()

    def getOptions(self):
        import cgi
        fieldStorage = cgi.FieldStorage()
        self.input = fieldStorage
        self.selectors={"count":"","order":"","camera":"","type":"","time":"","score":""}
        for key in self.input.keys():
            for filter in self.selectors:
                if key == filter:
                    self.selectors[filter] = fieldStorage.getvalue(key)

    def getFilterValues(self):
        self.currentFilters = {}
        for param in ['count','camera','type','score','time']:
            if param in self.input:
                if param == 'score':
                    score = self.input.getvalue(param)
                    if score != "0":
                        if len(score) > 3:
                            score = score[2:4]
                        else:
                            score = score[2:]
                            if int(score) < 10:
                                score = int(score)*10
                    self.currentFilters[param] = score
                    self.error.execute(f"SCORE: {score}",src=self.script)
                else:
                    self.currentFilters[param] = self.input.getvalue(param)
            else:
                self.currentFilters[param] = "none"

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

    def noEvents(self):
        if os.path.isfile(stub):
            with open(stub) as eventStub:
                url = "?action=config"
                thumbURL = "../img/not_available.jpg"
                caption = "No Events Found"
                data = eventStub.read()
                data = data.replace('##EVENT_URL##',url)
                data = data.replace('##EVENT_IMG##',thumbURL)
                data = data.replace('##EVENT_CAPTION##',caption)
                data = data.replace('##NEW##','')
        if data:
            return data

    def generateEventDiv(self,event):
        from datetime import datetime
        time = datetime.fromtimestamp(int(event['id'].split('.')[0]))
        ftime = str(self.convertTZ(str(time)))
        event['time'] = ftime[ftime.index('-')+1:]
        if os.path.isfile(stub):
            with open(stub) as eventStub:
                if str(event['ack']).lower() != "true":
                    newClass = "new"
                else:
                    newClass = "hidden"
                url = f"event.py?id={event['id']}"
                thumbURL = f"../events/{event['id']}/thumb.jpg"
                score = event['score']
                if len(score) > 3:
                    score = score[2:4]
                else:
                    score = event[2:]
                    if score < 10:
                        score = int(score)*10
                data = eventStub.read()
                data = data.replace('##URL##',url)
                data = data.replace('##IMG##',thumbURL)
                data = data.replace('##CAMERA##',event['camera'])
                data = data.replace('##OBJECT##', event['type'])
                data = data.replace('##SCORE##',f"{score}%")
                data = data.replace('##TIME##',event['time'][:-6])
                data = data.replace('##NEW##',newClass)
        if data:
            return data

    def getStub(self,stub):
        if os.path.isfile(stub):
            with open(stub) as Stub:
                return Stub.read()

    def getEvents(self,selectors):
        sql = "SELECT * FROM events"
        wheres = []
        where = ""
        sort = """ ORDER BY id DESC"""
        limit = 10
        for key in selectors:
            value=selectors[key]
            if value:
                if key == "count":
                    limit = value
                elif key == "sort":
                    if value == "newest":
                        sort = """ ORDER BY id DESC"""
                    elif value == "oldest":
                        sort = """ ORDER BY id ASC"""
                elif key == "score":
                    wheres.append(f"""{key}>{value}""")
                elif key == "time":
                    import datetime
                    time = datetime.datetime.fromtimestamp(value)
                    if value[-1] == "d":
                        time = time - datetime.timedelta(days=int(value.replace(value[-1],'')))
                    elif value[-1] == "h":
                        time = time - datetime.timedelta(hours=int(value.replace(value[-1],'')))
                    elif value[-1] == "w":
                        time = time - datetime.timedelta(weeks=int(value.replace(value[-1],'')))
                    elif value[-1] == "y":
                        days = int(value.replace(value[-1],'')) * 365
                        time = time - datetime.timedelta(days=days)
                        wheres.append(f"""{key}>{time}""")
                else:
                    wheres.append(f"""{key}='{value}'""")
        if wheres:
            x = 0
            for n in wheres:
                if x == 0:
                    where = "WHERE "
                else:
                    where += " AND "
                where += n
                x+=1
        if int(limit) > 0:
            where += f"{sort} LIMIT {limit}"
        else:
            where += f"{sort} LIMIT 10"
        sql = f"""SELECT * FROM events {where};"""
        from fetch import fetchEvent
        from sqlite import sqlite
        fsqlite = sqlite(db=self.fevr['db'])
        fsqlite.open()
        self.error.execute(sql,src=self.script)
        items = fsqlite.retrieve(sql)
        self.error.execute(f"# ITEMS: {len(items)}",src=self.script)
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
        if len(items) < 1:
            self.noResults = True
        return data

    def execute(self):
        from config import Config
        fconfig = Config()
        print('content-type: text/html; charset=UTF-8\n\n')
        if fconfig.exists:
            self.debug = fconfig.debug
            self.config = fconfig.config
            self.frigate = self.config['frigate']
            self.fevr = self.config['fevr']
            self.error.execute(self.frigate,src=self.script)
            self.error.execute(self.fevr,src=self.script)
            content = self.getEvents(self.selectors)
        else:
            content = self.getStub("/var/www/html/config.html")
        if self.noResults:
            content = self.noEvents()
        header = self.getStub("/var/www/html/stub/eventsHeader.html")
        footer = self.getStub("/var/www/html/stub/eventsFooter.html")
        from filter import eventFilter
        filters = eventFilter(self.frigate['url'],self.currentFilters)
        header = header.replace('##FILTERS##',filters.filters)
        print(f"{header}{content}{footer}")

def main():
    fevents = events()
    fevents.execute()
main()