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
        from os.path import basename
        self.script = basename(__file__)
        from logit import logit
        self.error = logit()
        import cgi
        self.getAction = ""
        self.jscript = ""
        self.input = cgi.FieldStorage()
        self.errorMsg = ""
        self.fatalErrorMsg = ""
        if self.input.getvalue('action'):
            self.getAction = self.input.getvalue('action')
            self.action()
        self.stub = "/var/www/html/stub"
        # Get our configuration
        from config import Config
        myConfig = Config()
        self.myConfig = myConfig.config
        from frigateConfig import frigateConfig
        self.error.execute(f"execute() : frigateConfig('{self.myConfig['frigate']['url']}')", src=self.script)
        self.fConfig = frigateConfig(self.myConfig['frigate']['url'])
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
        self.jscript = ""
        url = ""
        if self.getAction == "config":
            ext = ".html"
            self.jscript += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
            url = "../"
        else:
            url += f"{self.getAction}{ext}"
            for action in actions:
                if action == self.getAction:
                    if actions[action]:
                        for value in actions[action]:
                            if self.input.getvalue(value):
                                url += f"{value}={self.input.getvalue(value)}&"
            self.jscript += f"<script>document.getElementById('contentFrame').src = '{url}';</script>\n"
    def getCameraMenus(self):
        menuCamera = self.getStub(f"{self.stub}/menuCamera.html")
        menuObject = self.getStub(f"{self.stub}/menuObject.html")
        fullCameraMenu = ""
        for camera in self.fConfig.cameras:
            cameraMenu=f"{menuCamera}\n"
            cameraObjects =""
            for object in self.fConfig.cameras[camera]['objects']:
                cameraObjects+=f"{menuObject.replace('#OBJECT#',object)}"
            cameraMenu = cameraMenu.replace("#CAMERAOBJECTS#",cameraObjects)
            cameraMenu = cameraMenu.replace("#CAMERA#",camera)
            fullCameraMenu += cameraMenu
        return fullCameraMenu
    
    def genSettings(self):
        self.error.execute(f"genSettings() <- self.myConfig: {self.myConfig}",src=self.script)
        self.settingsMenu = self.getStub(f"{self.stub}/menuError.html")
        self.settingsMenu = self.settingsMenu.replace('##base##',self.myConfig['fevr']['base'])
        self.settingsMenu = self.settingsMenu.replace('##db##',self.myConfig['fevr']['db'])
        self.settingsMenu = self.settingsMenu.replace('##debug##',self.myConfig['fevr']['debug'])
        self.settingsMenu = self.settingsMenu.replace('##html##',self.myConfig['fevr']['html'])
        self.settingsMenu = self.settingsMenu.replace('##title##',self.myConfig['fevr']['title'])
        self.settingsMenu = self.settingsMenu.replace('##apiEventPath##',self.myConfig['frigate']['apiEventPath'])
        self.settingsMenu = self.settingsMenu.replace('##clipPath##',self.myConfig['frigate']['clipPath'])
        self.settingsMenu = self.settingsMenu.replace('##snapPath##',self.myConfig['frigate']['snapPath'])
        self.settingsMenu = self.settingsMenu.replace('##url##',self.myConfig['frigate']['url'])
        clock12 = "<option selected value='12'>12 Hour (am/pm)</option>\n"
        clock24 = "<option selected value='24'>24 Hour ('military time')</option>\n"
        if self.myConfig['fevr']['clock'] == '12':
            clock = f"{clock12} {clock24.replace('selected ','')}"
        elif self.myConfig['fevr']['clock'] == '24':
            clock = f"{clock12.replace('selected ','')} {clock24}"
        else:
            clock = f"{clock12.replace('selected ','')} {clock24}"
        self.settingsMenu = self.settingsMenu.replace('##clock##',clock)

        

    def mainPage(self):
        index = self.getStub(f"{self.stub}/index.html")
        
        menu=""
        if self.myConfig:
            try:
                menu=""
                if self.fConfig.frigateError or self.action == "config":
                    self.jscript += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
                    index = index.replace('##ACTION##',self.jscript)
                    self.errorMsg = "Your frigate server is unreachable at the moment.<br/>"
                else:
                    menu = self.getCameraMenus()
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
                    from os import environ
                    imgName=environ.get('FEVR_CONTAINER_NAME',"fevr")
                    errmsg =  f"\n\
                                Whoops!  fEVR can't take care of this one for you.\n\
                                Please run the following command:\n\
                                docker-compose exec {imgName} chown -R 100:101 /var/www/data && chmod -R 0770 /var/www/data"
                    self.jscript += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
                    index = index.replace('##ACTION##',self.jscript)
                    self.errorMsg = "Your frigate server is unreachable at the moment.<br/>"
                self.error.execute(errmsg,self.script)
            if not menu:
                menu = " <div class='menuitem menuspace'>\n\
                            CONFIG ERROR<br/>\n\
                            SEE SYSTEM LOGS<br/>\n\
                            <a href=?action=config>UPDATE SETTINGS</a>\n\
                        </div>"
                self.jscript += "<script>document.querySelector('#frigateErr').showModal()</script>\n"
                index = index.replace('##ACTION##',self.jscript)
                self.fatalErrorMsg = "Something went wrong.  See system logs or talk to your IT guy!.<br/>\n"
            index = index.replace('##MENU##',menu)
            index = index.replace('#FRIGATE#',self.myConfig['frigate']['url'])
            if self.fatalErrorMsg:
                index = index.replace("##ERROR##", self.fatalErrorMsg)
            else:
                index = index.replace("##ERROR##",self.settingsMenu)
                if self.errorMsg:
                    index = index.replace("##ERRMSG##",self.errorMsg)
                else:
                    index = index.replace("##ERRMSG##",'')
            return index

    def execute(self):
        
        # Generate our settings dialog
        self.genSettings()
        # Print the headers    
        index = self.header()
        #Print the page out
        index += self.mainPage()
        # If there's an action, do it.
        if self.jscript:
            action = self.jscript
        else:
            action = ""
        index = index.replace("##ACTION##",action)
        index = index.replace("##ERROR##",self.settingsMenu)
        self.error.execute(self.settingsMenu,src=self.script)

        print(index)

def main():
    fevr()

main()
