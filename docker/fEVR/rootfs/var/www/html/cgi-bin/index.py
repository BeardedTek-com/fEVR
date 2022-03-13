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
class fevr:
    def __init__(self):
        from logit import logit
        self.error = logit()
        import cgi
        self.getAction = ""
        self.script = ""
        self.input = cgi.FieldStorage()
        self.errorMsg = ""
        if self.input.getvalue('action'):
            self.getAction = self.input.getvalue('action')
            self.action()
        self.stub = "/var/www/html/stub"
        self.execute()

    def getStub(self,stub):
        with open(stub) as Stub:
            return Stub.read()

    def header(self):
        # Check to see if we should output something other than html headers.
        variant = {"rest":"application/json","text":"text/plain"}
        ctype = ""
        for loki in variant:
            if self.getAction:
                if loki == self.getAction:
                    ctype = variant[loki]
        if not ctype:
            ctype = "text/html"
        return f"content-type: {ctype}\n\n"

    def action(self):
        actions = {"event":['id','count'],"config":False}
        ext = ".py?"
        self.script = ""
        url = ""
        if self.getAction == "config":
            ext = ".html"
            self.script += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
            url = "../"
        else:
            url += f"{self.getAction}{ext}"
            for action in actions:
                if action == self.getAction:
                    if actions[action]:
                        for value in actions[action]:
                            if self.input.getvalue(value):
                                url += f"{value}={self.input.getvalue(value)}&"
            self.script += f"<script>document.getElementById('contentFrame').src = '{url}';</script>\n"
    def getCameraMenus(self,fConfig):
        menuCamera = self.getStub(f"{self.stub}/menuCamera.html")
        menuObject = self.getStub(f"{self.stub}/menuObject.html")
        fullCameraMenu = ""
        for camera in fConfig.cameras:
            cameraMenu=f"{menuCamera}\n"
            cameraObjects =""
            for object in fConfig.cameras[camera]['objects']:
                cameraObjects+=f"{menuObject.replace('#OBJECT#',object)}"
            cameraMenu = cameraMenu.replace("#CAMERAOBJECTS#",cameraObjects)
            cameraMenu = cameraMenu.replace("#CAMERA#",camera)
            fullCameraMenu += cameraMenu
        return fullCameraMenu
    def mainPage(self):
        frigateURL=""
        index = self.getStub(f"{self.stub}/index.html")
        from config import Config
        from frigateConfig import frigateConfig
        myConfig = Config()
        menu=""
        if myConfig:
            try:
                frigateURL = myConfig.config['frigate']['url']
                fConfig = frigateConfig(frigateURL)
                menu=""
                if fConfig.error or self.action == "config":
                    self.script += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
                    index = index.replace('##ACTION##',self.script)
                    self.errorMsg = "Your frigate server is unreachable at the moment.<br/>"
                    #menuError = self.getStub(f"{self.stub}/menuError.html")
                    #index = index.replace('##MENU##',"")
                    #index = index.replace("##ERROR##",menuError)
                else:
                    menu = self.getCameraMenus(fConfig)
            except:
                errmsg = "\nCouldn't get frigate's URL.  Looks like the permissions are wonky."
                try:
                    import os
                    mode=0o770
                    path="/var/www/data"
                    for root, dirs, files in os.walk(path):
                        for d in dirs:
                            os.chown(os.path.join(root,d),'100','101')
                            os.chmod(os.path.join(root, d), mode)
                            for f in files:
                                os.chown(os.path.join(root,f),'100','101')
                                os.chmod(os.path.join(root, f), mode)
                    errmsg = "\nYou lucky dog.  fEVR took care of it for you!!!"
                except:
                    index = index.replace('##MENU##','Config Error\nUpdate settings.')
                    from os import environ
                    imgName=environ.get('FEVR_CONTAINER_NAME',"fevr")
                    errmsg =  f"\n\
                                Whoops!  fEVR can't take care of this one for you.\n\
                                Please run the following command:\n\
                                docker-compose exec {imgName} chown -R 100:101 /var/www/data && chmod -R 0770 /var/www/data"
                self.error.execute(errmsg,self.script)
            if not menu:
                menu = " <div class='menuitem menuspace'>\n\
                            CONFIG ERROR<br/>\n\
                            SEE SYSTEM LOGS<br/>\n\
                            <a href=?action=config>UPDATE SETTINGS</a>\n\
                        </div>"
                frigateURL = "?action=config"
            menuError = self.getStub(f"{self.stub}/menuError.html")
            index = index.replace('##MENU##',menu)
            index = index.replace('#FRIGATE#',frigateURL)
            index = index.replace("##ERROR##",menuError) 
            return index

    def execute(self):
        # Print the headers    
        index = self.header()
        #Print the page out
        index += self.mainPage()
        # If there's an action, do it.
        if self.script:
            action = self.script
        else:
            action = ""
        index = index.replace("##ACTION##",action)
        if self.errorMsg:
            index = index.replace("#ERRORMSG#",self.errorMsg)
        else:
            index = index.replace("#ERRORMSG#","")

        print(index)

def main():
    fevr()

main()
