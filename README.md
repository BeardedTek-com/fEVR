# fEVR
## frigate Event Video Recorder - pronounced [fee-ver]
Written in python, pure HTML, pure javascript, and pure CSS.
I want to include the minimum amount of frameworks as this will prevent breakage due to upstream changes.

![fEVR-main](https://user-images.githubusercontent.com/93575915/151338205-c1e0f12e-1d8a-4c56-be59-d4b2c5e96bd7.png)


## Requirements:
- Home Assistant
- Frigate
## Recommended:
- Docker
- docker-compose

## Install
- clone the repository
```bash
git clone https://github.com/BeardedTek-com/fEVR.git
```
- edit docker-compose.yml - change ports if necessary
```yml
version: '2'
services:
  fevr:
    image: 'beardedtek/fevr:latest'
    restart: unless-stopped
    ports:
      - '80:80'
    volumes:
      - ./www:/var/www
```
- edit config.json

admin, adminPassword, and domain do nothing right now, but will be used in the future.
Ensure you change http://frigate.mydomain.com" to your frigate instance.

It MUST:
- be accessible by the fEVR web server.
- If fEVR is behind an SSL proxy, then frigate also must be served as https otherwise it will fail.

```bash
mv www/config/config-example.json www/config/config.json
```
```json
{
  "fevr"             :
  {
    "title"         : "frigate Event Video Recorder",
    "domain"        : "fevr.mydomain.com",
    "admin"         : "admin",
    "adminPassword" : "password"
  },
  "frigate"         :
  {
    "url"           : "http://frigate.mydomain.com",
    "apiEventPath"  : "/api/events/",
    "snapPath"      : "/snapshot.jpg",
    "clipPath"      : "/clip.mp4"
  }
}
```
- Build the docker image
Don't forget the trailing .
```bash
cd docker
sudo docker build -t beardedtek/fevr:latest .
```
- Start the container
```bash
cd ..
sudo docker-compose up

# This will show the apache error log.  If there is an error, it will show up here.
# This will be changed to a custom logging solution eventually, but I haven't written it yet.
sudo docker-compose exec fEVR tail -n 50 -f /var/log/apache2/error.log
```
## Main Display
![fEVR-main](https://user-images.githubusercontent.com/93575915/151338205-c1e0f12e-1d8a-4c56-be59-d4b2c5e96bd7.png)

## Menu
![fEVR-menu](https://user-images.githubusercontent.com/93575915/151338307-2df5f44d-2149-496a-850b-98e5b1c70b87.png)

## Event View
![fEVR-event](https://user-images.githubusercontent.com/93575915/151338353-ae2d7c21-8d6c-4ed8-aa8e-752b3914a9cb.png)

## Delete Event
At the moment, deleting an event will delete the associated files, but not the database entry.  This is for testing purposes.  The next update *should* include deleting the event from the database.
![fEVR-delete](https://user-images.githubusercontent.com/93575915/151338410-230f9512-4b0a-4a90-942c-0ee97d050983.png)

## Refresh Event
One *minor* bug is sometimes the clip doesn't play properly.  *Usually* refreshing the event will fix it.  However, if frigate deletes the event prior to you refreshing, the event will be lost.  This will be fixed soon, but for now it's acceptable behavior.  Remember, THIS IS NOT PRODUCTION READY!!! YOU MAY LOSE DATA!!!
![fEVR-refresh](https://user-images.githubusercontent.com/93575915/151338629-9616b08a-66f6-445f-a277-447009c2e683.png)


## Config
If you click the "config" menu item, basic configuration will be shown.  In the near future I plan on making configuration automatic throught Home Assistant's API and a couple forms.  Until then, a bit of knowledge of Home Assistant and Frigate is required.

## Pull Requests welcome!
Feel free to fork the project and submit pull requests.

## I would really like the UI rewritten for such and such a framework
If you wish to rewrite this with some fancy framework, please feel free to fork and submit a pull request against main.
We can then start a new branch for that framework.  
At this point, this branch of the UI will be supported only by you.

Hope you find this useful.
