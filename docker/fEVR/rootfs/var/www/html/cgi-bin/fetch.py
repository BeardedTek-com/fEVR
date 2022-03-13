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
class fetchEvent:
    def __init__(self,frigate,event,debug=False,thumbSize=180,location='/var/www/html/events/',db="/var/www/data/db/fEVR.sqlite"):
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        self.frigate = frigate
        self.event = event
        self.debug = debug
        self.thumbSize = thumbSize
        self.location = location
        self.eventPATH = f"{self.location}{self.event}"
        self.snapPATH = f"{self.eventPATH}{self.frigate['snapPath']}"
        self.thumbPATH= f"{self.eventPATH}/thumb.jpg"
        self.clipPATH = f"{self.location}{self.event}{self.frigate['clipPath']}"
        self.default = "/var/www/default/"
        self.Return = {}
        self.Return['event'] = self.event
        self.db = db
    def delEvent(self,db=True):
        import shutil
        path = f"{self.location}{self.event}"
        shutil.rmtree(path)
        if db:
            self.error.execute(f" delEvent() - DELETING DATABASE ENTRY",src=self.script)
            sql = f"""DELETE FROM events WHERE event='{self.event}';"""
            self.error.execute(f"delEvent() - {sql}",src=self.script)
            from sqlite import sqlite
            fsql = sqlite(db=self.db)
            fsql.open()
            self.error.execute(f" delEvent() - {fsql.execute(sql)}",src=self.script)
        else:
            self.error.execute(f" delEvent() - NOT DELETING DATABASE ENTRY",src=self.script)
    def ackEvent(self,value):
        sql = f"""UPDATE events SET ack='{value}' WHERE event='{self.event}';"""
        from sqlite import sqlite
        fsql = sqlite()
        fsql.open()
        self.error.execute(f" ackEvent() - {fsql.execute(sql)}",src=self.script)
    def getEvent(self):
        if not os.path.exists(self.thumbPATH):
            if not os.path.exists(self.eventPATH):
                os.makedirs(self.eventPATH)
            snapURL = f"{self.frigate['url']}{self.frigate['apiEventPath']}{self.event}{self.frigate['snapPath']}"
            clipURL = f"{self.frigate['url']}{self.frigate['apiEventPath']}{self.event}{self.frigate['clipPath']}"
            import requests
            snap = requests.get(snapURL, allow_redirects=True)
            open(self.snapPATH,'wb').write(snap.content)
            if 20 > os.path.getsize(self.snapPATH):
                self.Return['code'] = 20
                return self.Return
            self.resizeImg(self.snapPATH,self.thumbSize)
            clip = requests.get(clipURL, allow_redirects=True)
            open(self.clipPATH,'wb').write(clip.content)
        self.Return['code'] = 0
    def copyDefaults(self,type,item,destPATH):
        from shutil import copy
        src = f"{self.default}{type}/{item}"
        self.error.execute(f" copyDefaults() - {src} -> {destPATH}",src=self.script)
        copy(src,destPATH)
    def resizeImg(self,img,height=180,ratio=1.777777778):
        self.error.execute(f" resizeImage() - resizeImage({img},{height},{ratio})",src=self.script)
        from os.path import exists
        if exists(img):
            # Resizes an image from the filesystem
            width = int(height*ratio)
            size = (int(height*ratio),height)
            from PIL import Image
            picture = Image.open(img)
            thumb = picture.resize(size, Image.ANTIALIAS)
            thumb.save(self.thumbPATH,"JPEG", quality=75,optimize=True)
        else:
            self.error.execute(" resizeImage() - Can not resize snapshot.  Grabbing default!!!!!",src=self.script)
            self.copyDefaults("event","thumb.jpg",self.thumbPATH)
    def execute(self):
        self.getEvent()
        #return self.Return