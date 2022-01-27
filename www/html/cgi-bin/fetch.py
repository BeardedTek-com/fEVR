#!/usr/bin/python
#    fEVR (Frigate Event Video Recorder) Event Fetcher
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
    def __init__(self,frigate,event,thumbSize=180,location='/var/www/html/events/'):
        self.frigate = frigate
        self.event = event
        self.thumbSize = thumbSize
        self.location = location
        self.eventPATH = f"{self.location}{self.event}"
        self.snapPATH = f"{self.eventPATH}{self.frigate['snap']}"
        self.thumbPATH= f"{self.eventPATH}/thumb.jpg"
        self.clipPATH = f"{self.location}{self.event}{self.frigate['clip']}"
        self.default = "/var/www/default/"
        self.Return = {}
        self.Return['event'] = self.event
    def error(self,msg):
        from sys import stderr
        stderr.write(f"{str(msg)}\n")
    def delEvent(self):
        import shutil
        path = f"{self.location}{self.event}"
        shutil.rmtree(path)
        sql = f"""DELETE FROM events WHERE event='{self.event}'"""
        from sqlite import sqlite
        fsql = sqlite()
        fsql.execute(sql)
    def getEvent(self):
        if not os.path.exists(self.thumbPATH):
            if not os.path.exists(self.eventPATH):
                os.makedirs(self.eventPATH)
            snapURL = f"{self.frigate['localURL']}{self.frigate['api']}{self.event}{self.frigate['snap']}"
            clipURL = f"{self.frigate['localURL']}{self.frigate['api']}{self.event}{self.frigate['clip']}"
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
        self.error(f"{src} -> {destPATH}")
        copy(src,destPATH)
    def resizeImg(self,img,height=180,ratio=1.777777778):
        self.error(f"resizeImage({img},{height},{ratio})")
        from os.path import exists
        if exists(img):
            # Resizes an image from the filesystem
            width = int(height*ratio)
            size = (int(height*ratio),height)
            from PIL import Image as CompressImage
            picture = CompressImage.open(img)
            thumb = picture.resize(size)
            thumb.save(self.thumbPATH,"JPEG",optimize=True)
        else:
            self.error("Can not resize snapshot.  Grabbing default!!!!!")
            self.copyDefaults("event","thumb.jpg",self.thumbPATH)
    def execute(self):
        self.getEvent()
        #return self.Return