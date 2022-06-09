<p align="right" style="vertical-align:middle;"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Ffevr.video"><img src='https://fevr.video/img/share-fb.svg' style="height: 2em;"></a><a target="_blank" href="https://twitter.com/intent/tweet?url=http%3A%2F%2Ffevr.video&text=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-twitter.svg' style="height: 2em;"></a><a target="_blank" href="http://pinterest.com/pin/create/button/?url=http%3A%2F%2Ffevr.video&media=&description=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-pin.svg' style="height: 2em;"></a><a target="_blank" href="https://reddit.com/submit?url=https://fevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-reddit.svg' style="height: 2em;"></a><a target="_blank" href="http://www.linkedin.com/shareArticle?mini=true&url=http%3A%2F%2Ffevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-linkedin.svg' style="margin-right: 2em;height: 2em;"></a><a href="https://www.paypal.com/donate/?hosted_button_id=ZAHLQF24WAKES"><img src='https://fevr.video/img/paypal-donate.svg' style="height: 2em;"></a><a href="https://github.com/sponsors/BeardedTek-com"><img src='https://fevr.video/img/github-sponsor.svg' style="height: 2em;"></a><a href="https://tallyco.in/s/waqwip/"><img src='https://fevr.video/img/tallycoin-donate.png' style="height: 2em;"></a></p>

[![Build Status](https://drone2.beardedtek.com/api/badges/BeardedTek-com/fEVR/status.svg?ref=refs/heads/main)](https://drone2.beardedtek.com/BeardedTek-com/fEVR)

# fEVR - frigate Event Video Recorder
fEVR works along side of [frigate](https://frigate.video) and [home assistant](https://www.home-assistant.io/) to collect video and snapshots of objects detected using your existing camera systems.
![fEVR v0.6 Screenshot](https://user-images.githubusercontent.com/93575915/165704583-fec8e202-88b8-4ca2-9ff2-345c04da3722.png)

## Requirements:
- Frigate fully setup and working
- MQTT Broker (if you have frigate running, you have this) listening to 0.0.0.0
  - This caused me many headaches, hopefully it saves you some hair pulling.
    It allows mqtt clients on different subnets to access the broker.
    If setup within your local lan this does not alone open up external access, only to other subnets which already have access.
  - Example mosquitto.conf listener section if using port 1883
```
listener 1883 0.0.0.0
```

## Optional but nice:
- Tailscale Account (for secure remote access)
  - A docker-compose file will be included below for users not wanting tailscale
- Home Assistant (for notifications)
- Proxy server (nginx, traefik, caddy, etc)


# Installation

## Docker Compose:

docker-compose is the preferred installation method

### Edit .env file
Copy template.env to .env and adjust as necessary:
NOTE: The IP addresses in the .env file are for internal bridge networking and SHOULD NOT be on the same subnet as your home network.
The default values should serve you well.
```
### fEVR Setup ######################################################

# Changes the port fEVR runs on DEFAULT: 5090
FEVR_PORT=5090

# FLASK_ENV=development to put fEVR into Debug Mode
FLASK_ENV=development


### MQTT Client Setup ###############################################

MQTT_BROKER_IP=127.0.0.1
MQTT_BROKER_PORT=1883

# If there is no user/password, leave unset
MQTT_BROKER_USER=
MQTT_BROKER_PASS=

# Comma seperated string of MQTT topics to subscribe to.  LIMIT 5!!!
MQTT_TOPICS="frigate/+"


### Tailscale #######################################################

# Set to false to disable tailscale
TAILSCALE_ENABLE=true

TAILSCALE_TAGS=tag:fevr
TAILSCALE_HOSTNAME=fevr

# Obtain Auth Key from https://login.tailscale.com/admin/authkeys
TAILSCALE_AUTHKEY=tskey-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXX
```

```
version: '2.4'
services:
  fevr:
    image: ghcr.io/beardedtek-com/fevr:main
    container_name: fevr
    restart: unless-stopped
    privileged: true
#    ports:               #Uncomment to export port 5090 if you don't wish to use tailscale
#      - 5090:5090
    volumes:
      - ./events:/fevr/static/events
    environment:
      FLASK_ENV: ${FLASK_ENV:-development}
      FEVR_PORT: ${FEVR_PORT:-5090}
      TAILSCALE_ENABLE: ${TAILSCALE_ENABLE:-true}
      TAILSCALE_AUTHKEY: ${TAILSCALE_AUTHKEY}
      TAILSCALE_HOSTNAME: ${TAILSCALE_HOSTNAME:-fevr}
      TAILSCALE_TAGS: ${TAILSCALE_TAGS}
      MQTT_BROKER_IP: ${MQTT_BROKER_IP}
      MQTT_BROKER_PORT: ${MQTT_BROKER_PORT}
      MQTT_BROKER_USER: ${MQTT_BROKER_USER}
      MQTT_BROKER_PASS: ${MQTT_BROKER_PASS}
      MQTT_TOPICS: ${MQTT_TOPICS}
```

Bring the system up:
```
docker-compose up -d
```

# Setup
Procedure:

- Visit http(s)://<fevr_url>/setup
- Create admin account
- Login to new admin account
- Add all of your cameras.
  - It asks for both HLS and RTSP feeds.  Technically you don't need to enter anything but the camera name, but in a future release live view and frigate config will be enabled and will require these values
  - Click Next
- Configure Frigate
  - make one entry called 'frigate' (without the quotes) with your internally accessible frigate URL
  - make another entry called 'external' (without the quotes) with your externally accessible frigate URL
    - This is 100% Optional.  It does, however, enable live view outside your network.
    - If you don't have an externally accessible frigate URL, you can skip this step.
  - Click Next
- Configure MQTT Client
  - You need to generate an API Auth Key to configure this step.
    - This can be done on your profile page.  Click the Bearded Tek logo to drop down the menu and click on profile.
    - Scroll down and fill in the fields:
      - Name: Enter a name to remember this is for the mqtt client (mqtt_client)
      - ipv4 Address: OPTIONAL
      - Limit: Enter 0
        - If anything above 0 is entered, it is a limited use key.  It can only be used that many times to authenticate with the system.  Once it has been used x amount of times, it will be disabled.
  - Click Add and then Next
- Other is not populated yet, There are future plans for this page, just click Next again and you'll be brought to the main interface.


# Home Assistant Notifications
As of right now it's a bit complicated. For each notification type you want for each camera, a helper entity must be added.
For example, I have notifications setup for my driveway camera for person, animal, and vehicle, so I have the following helpers:
- fevrDrivewayAnimal
- fevrDrivewayCar
- fevrDrivewayPerson

The automation uses this helper entity for 2 purposes.
- As a motion sensor
  - If the helper is on, that means a notification is active
- As a pause for notifications
  - If the helper is on, it does not allow further notifications until it is turned off.
  - In the automation, this time can be adjusted to your liking

Here is the automation I'm currently using:
As displayed when:
- editing the automation via the UI
- click on overflow menu (3 dots)
- click Edit in YAML

NOTES:
- ***CAMERA*** is the camera name
- ***HELPER ENTITY*** is the entity you created for this notification
- ***YOUR FEVR URL*** is the url to your fevr instance

```
alias: fEVR <<CAMERA>> Person Alert
description: fEVR Object Detection Alerts
trigger:
  - platform: mqtt
    topic: frigate/events
condition:
  - condition: template
    value_template: '{{ trigger.payload_json["type"] == "end" }}'
  - condition: template
    value_template: |-
      {{
      trigger.payload_json["after"]["label"] == "person"
      }}
  - condition: template
    value_template: |-
      {{
      trigger.payload_json["after"]["top_score"] > 0.76
      }}
  - condition: template
    value_template: |-
      {{
      trigger.payload_json["after"]["camera"] == "<<CAMERA>>"
      }}
action:
  - choose:
      - conditions:
          - condition: state
            state: 'off'
            entity_id: input_boolean.fevrbackyardperson
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
                    title: Clip
                    uri: >-
                      <<YOUR FEVR URL>>/event/{{trigger.payload_json['after']['id']}}/snap
                  - action: URI
                    title: Snapshot
                    uri: >-
                      <<YOUR FEVR URL>>/event/{{trigger.payload_json['after']['id']}}/snap
                image: >-
                  <<YOUR FEVR URL>>/static/events/{{trigger.payload_json['after']['id']}}/snapshot.jpg
                tag: '{{trigger.payload_json["after"]["id"]}}'
                alert_once: true
          - service: input_boolean.turn_on
            data: {}
            target:
              entity_id: input_boolean.<<HELPER ENTITY>>
          - delay:
              hours: 0
              minutes: 1
              seconds: 0
              milliseconds: 0
          - service: input_boolean.turn_off
            data: {}
            target:
              entity_id: input_boolean.<<HELPER ENTITY>>
    default: []
mode: single
```
