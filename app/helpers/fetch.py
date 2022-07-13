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
from app.helpers.logit import logit

class Fetch:
    def __init__(self,path,eventid,frigate,thumbsize=180):
        self.path = path
        self.event = eventid
        self.frigate = frigate
        self.thumbSize = thumbsize
        self.thumbPATH = f"{self.path}/thumb.jpg"
        self.clipPATH = f"{self.path}/clip.mp4"
        self.snapPATH = f"{self.path}/snapshot.jpg"
        self.snap = f"{self.frigate}/api/events/{eventid}/snapshot.jpg".replace("//api","/api")
        self.clip = f"{self.frigate}/api/events/{eventid}/clip.mp4".replace("//api","/api")
        self.source = "fEVR | FETCH"
        self.getEvent()
    def getEvent(self):
        logit.execute(f"Getting {self.event}",src=self.source)
        try:
            if not os.path.exists(self.thumbPATH):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                else:
                    rVal = {"error":3,"msg":f"{self.path} already exists"}
                with open(self.snapPATH,'wb') as snap:
                    logit.execute(f"Fetching {self.snap} into {self.snapPATH}",src=self.source)
                    snap.write(requests.get(self.snap, allow_redirects=True).content)
                resize = self.resizeImg(self.snapPATH,self.thumbSize)
                if resize["error"] != 0:
                    rVal = {"error":4,"msg":f"{self.snapPATH} resize failed"}
                with open(self.clipPATH,'wb') as clip:
                    logit.execute(f"Fetching {self.clip} into {self.snapPATH}",src=self.source)
                    clip.write(requests.get(self.clip, allow_redirects=True).content)
            else:
                rVal = {"error": 1,"msg":f"{self.thumbPATH} already exists"}
            rVal = {"error": 0,"msg":f"Fetched {self.event} from {self.frigate}"}
        except Exception as err:
            rVal = {"error": 1,"msg":f"Failed to fetch {self.event} from frigate at {self.frigate}.  Check settings or maybe Frigate is down?"}
        logit.execute(rVal['msg'] if rVal['error'] == 0 else rVal,src=self.source)
        return rVal

    def resizeImg(self,img,height=180,ratio=1.777777778):
        # Resizes an image from the filesystem
        if os.path.exists(img):
            Image.open(img).resize((int(height*ratio),height), Image.ANTIALIAS).save(self.thumbPATH,"JPEG", quality=75,optimize=True)
            rVal = {"error":0,"msg": "Image Resized"}
        else:
            rVal = {"error":1,"msg": "Image path does not exist"}
        logit.execute(rVal['msg'] if rVal['error'] == 0 else rVal,src=self.source)
        return rVal
        
        