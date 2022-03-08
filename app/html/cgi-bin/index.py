#!/usr/bin/python
print('content-type: text/html\n\n')
from config import Config
fevr = Config()
if fevr:
    from frigateConfig import frigateConfig
    frigate = fevr.config['frigate']
    fConfig = frigateConfig(frigate['url'])
    with open('/var/www/html/stub/index.stub') as indexStub:
        index = indexStub.read()
    with open('/var/www/html/stub/menuCamera.stub') as menuCameraStub:
        menuCameraItem = menuCameraStub.read()
    with open('/var/www/html/stub/menuObject.stub') as menuObjectStub:
        menuObjectItem = menuObjectStub.read()
        menu = ""
    for camera in fConfig.cameras:
        menu += f"{menuCameraItem}\n"
        for object in fConfig.cameras[camera]['objects']:
            menu+= f"{menuObjectItem.replace('#OBJECT#',object)}"
        menu = menu.replace("#CAMERA#",camera)
    index = index.replace('##MENU##',menu)
    index = index.replace('#FRIGATE#',frigate['url'])
    print(index)

