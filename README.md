# fEVR
## frigate Event Video Recorder - pronounced [fee-ver]
Written in python, pure HTML, pure javascript, and pure CSS.
I want to include the minimum amount of frameworks as this will prevent breakage due to upstream changes.

### Cloud Instances of fEVR
- I will be offering cloud instances of fEVR starting on March 31st.
- See [My Sponsorship Page](https://github.com/sponsors/BeardedTek-com) for more details.
#### Cloud BETA Testing
- If you would like to beta test this feature, please let me know by submitting an issue.

![fEVR-0 3 3 Main](https://user-images.githubusercontent.com/93575915/155628108-99e39877-b57b-4c13-ba62-fcf1a04941ee.png)

## Known Bugs
- Modals do not work properly in Firefox < 98
  - Either upgrade to the Firefox Beta, wait for Firefox 98 to come out, or use a chromium derivative.
  - For now Chromium derivatives work
- [See Issues for other known bugs.](https://github.com/BeardedTek-com/fEVR/issues)

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
version: '3'
services:
  fevr:
    image: ghcr.io/beardedtek/fevr-standalone:main
    container_name: fevr-alpine
    restart: unless-stopped
    ports:
      - '8003:8001'
      - '8004:8002'
    volumes:
     - ./data/events:/var/www/html/events ##OPTIONAL: save events to a local folder
     - ./data/fEVR.sqlite:/var/www/db/fEVR.sqlite ##OPTIONAL: save database file
     - ./data/config.json:/var/www/config/config.json ##OPTIONAL: save config file locally
     #- ./app:/var/www # FOR DEVELOPMENT - Exposes the entire stack to a local volume
     # If you go with this option, take the following actions:
     # git clone https://github.com/beardedtek-com/fevr
     # cd fevr
     # sudo chmod -R 100:101 app
     # edit docker-compose.yml and comment out or remove first 3 volume definitions,
     # uncomment 4th volume definition and run the container:
     # docker-compose up -d
     
# Uncomment the following to map to an NFS share
#    - nfsvolume:/var/www/html/events ##OPTIONAL: save events to an NFS volume
#volumes:
#  nfsvolume:
#    driver_opts:
#      type: "nfs"
#      o: "addr=<your_nas_ip>,nfsvers=4" # Make sure to change to your NFS server's address
#     #o: "addr=<your_nas_ip>,rw,nfsvers=4" < SOME NFS SHARES REQUIRE THIS!!!
#      device: ":/path/to/your/nfs/share"
```
- Follow the instructions in docker-compose.yml
- Run the container with docker-compose:
```
docker-compose up -d
```
- View apache2 error log
```
docker-compose exec fevr tail -n 50 -f /var/log/apache2/error*
```
- Configure Home Assistant Automation to feed the fevr with data:

### Home Assistant Automation v2
[v2 of the Home Assistant Automation](https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/docs/automation.yml) adds a "break" using an input boolean helper.
```yaml
- id: '1643335976518'
  alias: fEVR Alerts 2.0
  description: fEVR Object Detection Alerts
  trigger:
  - platform: mqtt
    topic: frigate/events
  condition:
  - condition: template
    value_template: '{{ trigger.payload_json["type"] == "end" }}'
  - condition: template
    value_template: "{{ trigger.payload_json[\"after\"][\"label\"] == \"person\" or\n\
      \   trigger.payload_json[\"after\"][\"label\"] == \"car\" or\n   trigger.payload_json[\"\
      after\"][\"label\"] == \"horse\" \n}}"
  - condition: template
    value_template: '{{ trigger.payload_json["after"]["top_score"] > 0.76 }}'
  action:
  - service: rest_command.fevr
    data:
      debug: 'yes'
      event: '{{trigger.payload_json[''after''][''id'']}}'
      camera: '{{trigger.payload_json[''after''][''camera'']}}'
      type: '{{trigger.payload_json[''after''][''label'']}}'
      clip: '{{trigger.payload_json[''after''][''has_clip'']}}'
      snap: '{{trigger.payload_json[''after''][''has_snapshot'']}}'
      score: '{{trigger.payload_json[''after''][''top_score'']}}'
      updated: '{{as_timestamp(now())}}'
  - choose:
    - conditions:
      - condition: state
        entity_id: input_boolean.notification_pause
        state: 'off'
      sequence:
      - service: notify.mobile_app_sg20plus
        data:
          message: '{{ trigger.payload_json["after"]["label"] | title }} Detected'
          data:
            notification_icon: mdi:cctv
            ttl: 0
            priority: high
            sticky: true
            actions:
            - action: URI
              title: Event Viewer
              uri: https://hpf.jeandr.net/cgi-bin/hasspyfrigate.py?id={{trigger.payload_json['after']['id']}}&camera={{trigger.payload_json['after']['camera']}}&bbox=true&url=https://hass.jeandr.net/api/frigate/notifications/&time={{trigger.payload_json['after']['start_time']}}&css=../css/hasspyfrigate.css#
            - action: URI
              title: fEVR (int)
              uri: http://192.168.2.240/
            - action: URI
              title: fEVR (ext)
              uri: https://fEVR.jeandr.net/
            image: /api/frigate/notifications/{{trigger.payload_json['after']['id']}}/snapshot.jpg?bbox=1
            tag: '{{trigger.payload_json["after"]["id"]}}'
            alert_once: true
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.notification_pause
      - delay:
          hours: 0
          minutes: 2
          seconds: 0
          milliseconds: 0
      - service: input_boolean.turn_off
        target:
          entity_id: input_boolean.notification_pause
    default: []
  mode: single
```

## Screenshots

### Main Display
![fEVR-0 3 3 Main](https://user-images.githubusercontent.com/93575915/155628975-d61614ef-843c-4f82-ab99-add7e9de04b6.png)

### Menu
![fEVR-0 3 3 Menu](https://user-images.githubusercontent.com/93575915/155628992-2fffd3d6-f5f6-407b-91b9-2f2a3c6a27bd.png)

### Event View
![fEVR-0 3 3 Event Detail](https://user-images.githubusercontent.com/93575915/155629005-1f20d47e-a3c5-4bd0-b169-b87dc2848def.png)

### Event Acknowledgement (shows or hides "new" label)
More to come on this in future releases
![fEVR-0 3 3 Acknowledge Event](https://user-images.githubusercontent.com/93575915/155629269-d8cd6581-88b5-4091-9cc2-546f859aadad.png)
![fEVR-0 3 3 Event Detail Acknowledged](https://user-images.githubusercontent.com/93575915/155629282-885b3159-685f-4864-a303-6cc30309b46f.png)
![fEVR-0 3 3 Unacknowledge Event](https://user-images.githubusercontent.com/93575915/155629293-1fd25823-7938-416d-b3c4-c0e12841a8ba.png)


### Delete Event
![fEVR-0 3 3 Delete Event](https://user-images.githubusercontent.com/93575915/155629034-19fda859-cf84-4375-969c-68c52e414561.png)

### Refresh Event
![fEVR-0 3 3 Refresh Event](https://user-images.githubusercontent.com/93575915/155629084-54474c5c-bda1-4379-8751-c127faba3cd1.png)

### Config
![fEVR-0 3 3 Config-1](https://user-images.githubusercontent.com/93575915/155629116-7260056a-1d4b-4490-bacb-173a15477136.png)
![fEVR-0 3 3 Config-2](https://user-images.githubusercontent.com/93575915/155629125-f45f0ffb-a283-4ea5-a7f4-74882de10c38.png)


## Pull Requests welcome!
Feel free to fork the project and submit pull requests.

Hope you find this useful.
