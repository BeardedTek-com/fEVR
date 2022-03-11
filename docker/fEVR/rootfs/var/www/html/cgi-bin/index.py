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
        url += f"{self.getAction}{ext}"
        for action in actions:
            if action == self.getAction:
                if actions[action]:
                    for value in actions[action]:
                        if self.input.getvalue(value):
                            url += f"{value}={self.input.getvalue(value)}&"
        self.script += f"<script>document.getElementById('contentFrame').src = '{url}';</script>\n"
    def mainPage(self):
        from config import Config
        from frigateConfig import frigateConfig
        myConfig = Config()
        if myConfig:
            frigateURL = myConfig.config['frigate']['url']
            fConfig = frigateConfig(frigateURL)
            index = self.getStub(f"{self.stub}/index.html")
            menuCamera = self.getStub(f"{self.stub}/menuCamera.html")
            menuObject = self.getStub(f"{self.stub}/menuObject.html")
            menu=""
            if fConfig.error or self.action == "config":
                self.script += "<script>document.querySelector('#frigateErr').close()</script>\n"
                #menuError = self.getStub(f"{self.stub}/menuError.html")
                #index = index.replace('##MENU##',"")
                #index = index.replace("##ERROR##",menuError)
            else:
                menuError = self.getStub(f"{self.stub}/menuError.html")
                for camera in fConfig.cameras:
                    menu+=f"{menuCamera}\n"
                    for object in fConfig.cameras[camera]['objects']:
                        menu+=f"{menuObject.replace('#OBJECT#',object)}"
                    menu = menu.replace("#CAMERA#",camera)
                index = index.replace('##MENU##',menu)
                index = index.replace("##ERROR##",menuError) 
            index = index.replace('#FRIGATE#',frigateURL)
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
        print(index)

def main():
    fevr()

main()
