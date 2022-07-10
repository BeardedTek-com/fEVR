#    This code is a portion of frigate Event Video Recorder (fEVR)
#
#    Copyright (C) 2021-2022  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU AfferoGeneral Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from PIL import Image
import requests

class Fetch:
    def __init__(self,path,eventid,frigate,thumbsize=180):
        self.path = path
        self.event = eventid
        self.frigate = frigate
        self.thumbSize = thumbsize
        self.thumbPATH = f"{self.path}/thumb.jpg"
        self.clipPATH = f"{self.path}/clip.mp4"
        self.snapPATH = f"{self.path}/snapshot.jpg"
        self.snap = f"{self.frigate}api/events/{eventid}/snapshot.jpg"
        self.clip = f"{self.frigate}api/events/{eventid}/clip.mp4"
        self.getEvent()
    def getEvent(self):
        failure = "none"
        if not os.path.exists(self.thumbPATH):
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            open(self.snapPATH,'wb').write(requests.get(self.snap, allow_redirects=True).content)
            resize = self.resizeImg(self.snapPATH,self.thumbSize)
            if resize != "OK":
                retval="resize image"                
            open(self.clipPATH,'wb').write(requests.get(self.clip, allow_redirects=True).content)
            if failure != "none":
                return f"Failed to retrieve {self.event} from frigate at {self.frigate}: {failure}"
            else:
                return f"Got {self.event} from frigate at {self.frigate}"
    def resizeImg(self,img,height=180,ratio=1.777777778):
        if os.path.exists(img):
            # Resizes an image from the filesystem
            if os.path.exists(img):
                Image.open(img).resize((int(height*ratio),height), Image.ANTIALIAS).save(self.thumbPATH,"JPEG", quality=75,optimize=True)
                return "OK"
            else:
                return "fetch.py | resizeImg(): Image Path Does Not Exist"
        