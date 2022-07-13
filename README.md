<p align="right" style="vertical-align:middle;"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Ffevr.video"><img src='https://fevr.video/img/share-fb.svg' style="height: 2em;"></a><a target="_blank" href="https://twitter.com/intent/tweet?url=http%3A%2F%2Ffevr.video&text=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-twitter.svg' style="height: 2em;"></a><a target="_blank" href="http://pinterest.com/pin/create/button/?url=http%3A%2F%2Ffevr.video&media=&description=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-pin.svg' style="height: 2em;"></a><a target="_blank" href="https://reddit.com/submit?url=https://fevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-reddit.svg' style="height: 2em;"></a><a target="_blank" href="http://www.linkedin.com/shareArticle?mini=true&url=http%3A%2F%2Ffevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-linkedin.svg' style="margin-right: 2em;height: 2em;"></a><a href="https://www.paypal.com/donate/?hosted_button_id=ZAHLQF24WAKES"><img src='https://fevr.video/img/paypal-donate.svg' style="height: 2em;"></a><a href="https://github.com/sponsors/BeardedTek-com"><img src='https://fevr.video/img/github-sponsor.svg' style="height: 2em;"></a><a href="https://tallyco.in/s/waqwip/"><img src='https://fevr.video/img/tallycoin-donate.png' style="height: 2em;"></a></p>

---

# fEVR - frigate Event Video Recorder

[![license](https://img.shields.io/github/license/beardedtek-com/fevr)](https://github.com/BeardedTek-com/fevr/blob/0.1.0/LICENSE)
[![telegram](https://img.shields.io/badge/Support-Telegram-blue)](https://t.me/BeardedTekfEVR)
[![Discussions](https://img.shields.io/github/discussions/beardedtek-com/fevr)](https://github.com/BeardedTek-com/fEVR/discussions)
[![commits since last release](https://img.shields.io/github/commits-since/beardedtek-com/fevr/latest?include_prereleases)](https://github.com/BeardedTek-com/fEVR/releases)
[![Build Status](https://drone.beardedtek.com/api/badges/BeardedTek-com/fEVR/status.svg)](https://drone.beardedtek.com/BeardedTek-com/fEVR)
[![Image Size](https://img.shields.io/docker/image-size/beardedtek/fevr)](https://hub.docker.com/r/beardedtek/fevr)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fbeardedtek-com%2Ffevr)](https://twitter.com/intent/tweet?url=https%3A%2F%2Ffevr.video&text=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder)
[![twitter-follow](https://img.shields.io/twitter/follow/beardedtek?style=social)](https://twitter.com/intent/user?screen_name=beardedtek)


fEVR works along side of [frigate](https://frigate.video) to collect video and snapshots of objects detected using your existing camera systems.
<p align="center">
<img alt="fEVR v0.6 Screenshots" src="https://user-images.githubusercontent.com/93575915/165704583-fec8e202-88b8-4ca2-9ff2-345c04da3722.png">
</p>
<p align="center">
fEVR v0.6 Screenshots
</p>

# Own Your Home's Security

fEVR allows you to own your home's camera system.  Instead of paying multiple cloud providers varying rates to perform object detection and recording, bring them all into fEVR in your very own open source self-hosted solution!  Google, Wyze, Ring, and varying Tuya based cameras all use your data AND want to charge you to store it in the cloud.
<p align="center">
<img alt="Feature comparison to leading cloud event detection providers" src="docs/images/features.webp">
</p>
<p align="center">
Feature comparison to leading cloud event detection providers
</p>

---

# Requirements:
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

---

# Documentation
## **[Main API Calls](docs/API.md)**
## **[mqtt_client](docs/MQTT_CLIENT.md)**
---

# Installation

## Docker Compose:
docker-compose is the preferred installation method

### Environment Variables
The following environment variables can be used to configure fEVR:
If not set, configuration can be done via the Web UI.

- FEVR_TRANSPORT
  - http or https
- FEVR_URL
  - defaults to 'fevr'
- FEVR_PORT
  - defaults to 5090
- FEVR_DEVELOPMENT
  - If set to true, it will use the builtin flask server in development/debug mode
  - If set to false or unset, it will use uwsgi server.
- TAILSCALE_ENABLE
  - Enable or disable tailscale functionality
  - [Sign up for tailscale](https://login.tailscale.com/start) prior to use.
- TAILSCALE_TAGS
  - Use tailscale tags
  - To use tags, you must [set them up](https://login.tailscale.com/admin/acls) first.
- TAILSCALE_HOSTNAME
  - Set hostname for tailscale
-TAILSCALE_AUTHKEY
  - You must [generate an auth key](https://login.tailscale.com/admin/settings/keys) first.

### Edit .env file
Copy template.env to .env and adjust as necessary:
NOTE: The IP addresses in the .env file are for internal bridge networking and SHOULD NOT be on the same subnet as your home network.
The default values should serve you well.
```
### fEVR Setup ######################################################

# Set fevr in development mode using built in flask server (true/false)
FEVR_DEVELOPMENT=false

# Changes the port fEVR runs on DEFAULT: 5090
FEVR_PORT=5090

# Should be set to image name to use local transport, or an accessible url to feed an external instance of fEVR 
FEVR_URL=fevr

# Set to http or https depending on use.  For internal docker network, use http.
FEVR_TRANSPORT=http

### MQTT Client Setup ###############################################

MQTT_BROKER=mqtt
MQTT_BROKER_PORT=1883

# If there is no user/password, leave unset
MQTT_BROKER_USER=
MQTT_BROKER_PASSWORD=

# Comma seperated string of MQTT topics to subscribe to.  LIMIT 5!!!
MQTT_TOPICS="frigate/+"

MQTT_VERBOSE_LOGGING=false

# Obtain this key from http(s)://<fevr_url:port>/profile or leave unset to use web ui setup values
MQTT_APIAUTH_KEY=


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
    image: ghcr.io/beardedtek-com/fevr:0.6
    container_name: fevr
    restart: unless-stopped
    privileged: true
    ports:
      - 5090:${FEVR_PORT:-5090}
    volumes:
      - /export/fevr:/fevr/app/static/events
      - /export/fevr/data:/fevr/app/data
      - ./fevr/varlib:/var/lib
    depends_on:
      - mqtt
      - frigate
    environment:
      FEVR_DEVELOPMENT: ${FEVR_DEVELOPMENT:-false}
      FEVR_URL: ${FEVR_URL}
      FEVR_PORT: ${FEVR_PORT}
      TAILSCALE_ENABLE: ${TAILSCALE_ENABLE:-true}
      TAILSCALE_AUTHKEY: ${TAILSCALE_AUTHKEY}
      TAILSCALE_HOSTNAME: ${TAILSCALE_HOSTNAME:-fevr}
      TAILSCALE_TAGS: ${TAILSCALE_TAGS}
      MQTT_BROKER: ${MQTT_BROKER:-mqtt}
      MQTT_BROKER_PORT: ${MQTT_BROKER_PORT}
      MQTT_BROKER_USER: ${MQTT_BROKER_USER}
      MQTT_BROKER_PASSWORD: ${MQTT_BROKER_PASSWORD}
      MQTT_TOPICS: ${MQTT_TOPICS:-frigate/+}
      MQTT_VERBOSE_LOGGING: ${MQTT_VERBOSE_LOGGING:-true}
      MQTT_APIAUTH_KEY: ${MQTT_APIAUTH_KEY}
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
- Other is not populated yet, There are future plans for this page, just click Next again and you'll be brought to the main interface.
- Generate API Key for mqtt_client
  - mqtt_client authenticates with fEVR using a 128 character API Key.
  - You can generate an API Key from `/profile` or click on the beard icon to drop down the menu, and click Profile.
  - Here you can view any API keys you have generated in the past and generate a new one.
  - There are 3 fields to fill out:
    - Name: A unique name to identify this key (no duplicates allowed)
    - IPv4 Address: Not used as of now but required to be a valid IP or network (without cidr notation)
      - Enter 0.0.0.0 to future proof.
    - Login Count: this can be used to limit the amount of times this API Key can be used.  While not used at the moment, it will function as the base of a limited login solution (say one time passwords for law enforcement and the like)
      - Enter 0 for unlimited usage
  - Configure mqtt_client
    - Once you have your API Key you can generate your config file for the mqtt_client.
      - [See mqtt_client docs here](docs/MQTT_CLIENT.md) for an example
    - This should be automated further in 0.6.1

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
