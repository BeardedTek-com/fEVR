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
        