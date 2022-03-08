#!/usr/bin/python
class frigateConfig:
    def __init__(self,frigateURL):
        self.url = frigateURL
        self.configAPI = "/api/config"
        self.cameras = {}
        self.getConfig()
        self.getCameras()
    def getConfig(self):
        configURL = f"{self.url}{self.configAPI}"
        import requests
        frigateConfig = requests.get(configURL, allow_redirects=True)
        import json
        self.frigateConfig = json.loads(frigateConfig.content)
    def getCameras(self):
        for camera in self.frigateConfig['cameras']:
            self.cameras[camera] = {}
            self.cameras[camera]['objects'] = []
            for object in self.frigateConfig['cameras'][camera]['record']['events']['objects']:
                self.cameras[camera]['objects'].append(object)
