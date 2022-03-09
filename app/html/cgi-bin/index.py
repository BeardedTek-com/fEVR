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
print('content-type: text/html\n\n')
from config import Config
fevr = Config()
if fevr:
    from frigateConfig import frigateConfig
    frigate = fevr.config['frigate']
    fConfig = frigateConfig(frigate['url'])
    with open('/var/www/html/stub/index.html') as indexStub:
        index = indexStub.read()
    with open('/var/www/html/stub/menuCamera.html') as menuCameraStub:
        menuCameraItem = menuCameraStub.read()
    with open('/var/www/html/stub/menuObject.html') as menuObjectStub:
        menuObjectItem = menuObjectStub.read()
        menu = ""
    if not fConfig.error:
        for camera in fConfig.cameras:
            menu += f"{menuCameraItem}\n"
            for object in fConfig.cameras[camera]['objects']:
                menu+= f"{menuObjectItem.replace('#OBJECT#',object)}"
            menu = menu.replace("#CAMERA#",camera)
        index = index.replace('##MENU##',menu)
        index = index.replace("##ERROR##","")
    else:
        with open('/var/www/html/stub/menuError.html') as menuError:
            error = menuError.read()
        index = index.replace('##MENU##',"")
        index = index.replace("##ERROR##",error)
    index = index.replace('#FRIGATE#',frigate['url'])
    print(index)

