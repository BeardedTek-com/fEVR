<span align="left" style="width:45%;vertical-align:middle; padding=1em;"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Ffevr.video"><img src='https://fevr.video/img/share-fb.svg' style="height: 2em;"></a><a target="_blank" href="https://twitter.com/intent/tweet?url=http%3A%2F%2Ffevr.video&text=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-twitter.svg' style="height: 2em;"></a><a target="_blank" href="http://pinterest.com/pin/create/button/?url=http%3A%2F%2Ffevr.video&media=&description=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-pin.svg' style="height: 2em;"></a><a target="_blank" href="https://reddit.com/submit?url=https://fevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-reddit.svg' style="height: 2em;"></a><a target="_blank" href="http://www.linkedin.com/shareArticle?mini=true&url=http%3A%2F%2Ffevr.video&title=AI%20Object%20Detection%20with%20fEVR%20-%20frigate%20Event%20Video%20Recorder"><img src='https://fevr.video/img/share-linkedin.svg' style="height: 2em;"></a></p><span align="right" style="width:45%;vertical-align:middle; padding=1em;"><a href="https://www.paypal.com/donate/?hosted_button_id=ZAHLQF24WAKES"><img src='https://fevr.video/img/paypal-donate.svg' style="height: 2em;"></a><a href="https://github.com/sponsors/BeardedTek-com"><img src='https://fevr.video/img/github-sponsor.svg' style="height: 2em;"></a><a href="https://tallyco.in/s/waqwip/"><img src='https://fevr.video/img/tallycoin-donate.png' style="height: 2em;"></a></p></div>

# fEVR - frigate Event Video Recorder
fEVR works along side of [frigate](https://frigate.video) and [home assistant](https://www.home-assistant.io/) to collect video and snapshots of objects detected using your existing camera systems.

## Notable Mentions
<a href="https://selfhosted.show/67"><img src="https://assets.fireside.fm/file/fireside-images/podcasts/images/7/7296e34a-2697-479a-adfb-ad32329dd0b0/cover_small.jpg?v=2" style="height:3em;"></a> <a href="https://linuxunplugged.com/451"><img src="https://assets.fireside.fm/file/fireside-images/podcasts/images/f/f31a453c-fa15-491f-8618-3f71f1d565e5/cover_small.jpg?v=3" style="height:3em;"></a>

## [Value 4 Value](https://www.entrepreneurability.nl/value-for-value-model/?lang=en)
If you find value in this, please give back.  Filing a [bug report, suggestion or feature request](https://github.com/BeardedTek-com/fEVR/issues/new/choose), a high five, share us on social media, a kind note, or even a donation goes a long way to making the upkeep of open source software more enjoyable for the community as a whole.

## Screenshot
![fEVR v0.5.1 Screenshot](https://fevr.video/img/screenshot.png)


## Features
- Stores video independently of frigate
- Home Assistant generates notifications and makes a RESTful command to fEVR to grab data from frigate
- fEVR stores, sorts, and makes browsing frigate events a snap.

## Support
- [The Official fEVR.video website](https://fevr.video)
- [Our Discussion on Github](https://github.com/BeardedTek-com/fEVR/discussions)
- [File an Issue on Github](https://github.com/BeardedTek-com/fEVR/issues)


### Cloud Instances of fEVR
- I will be offering cloud instances of fEVR soon.
- [Click here](https://fevr.video) for more details.
### Cloud BETA Testing
- If you would like to beta test this feature, please let me know by submitting an issue.

## Known Bugs
- [See Issues for known bugs.](https://github.com/BeardedTek-com/fEVR/issues)

## Requirements:
- [home assistant](https://home-assistant.io)
- [frigate](https://frigate.video)

## Install
The easiest and recommended method of install is docker-compose.
- Included is a container running tailscale to securely access fEVR.  This is not 100% necessary, but far more secure.

- Create .env file
```
cp template.env .env
nano .env
```
- Edit .env file and
```
# Bridge Network Details
NETWORK_NAME=beardnet
NETWORK_SUBNET=192.168.200.0/24
NETWORK_GATEWAY=192.168.200.1

# Tailscale Container Variables
TAILSCALE_IP=192.168.200.3
TAILSCALE_IMAGE=ghcr.io/beardedtek-com/tailscale:main
TAILSCALE_CONTAINER_NAME=tailscale-devel
TAILSCALE_CONTEXT=./docker/tailscale/
TAILSCALE_DATA=./vol/tailscale/data
TAILSCALE_VAR_LIB=./vol/tailscale/var_lib
TAILSCALE_COMMAND=/opt/tailscale/tailscale

# fEVR Container Variables
FEVR_IP=192.168.200.2
FEVR_IMAGE=ghcr.io/beardedtek-com/fevr:main
FEVR_CONTAINER_NAME=fevr-devel
FEVR_CONTEXT=./docker/fEVR/
FEVR_DEBUG=true
FEVR_TITLE=Home
FRGIGATE_URL=http://192.168.2.240:5000

# OPTIONAL NAS
NAS_IP=192.168.18.10
NAS_EVENTS=/export/fevr
NAS_DATA=/export/fevr_data

# MQTT
MQTT_BROKER_URL=192.168.18.10
MQTT_BROKER_PORT=1883
MQTT_USER=
MQTT_PASS=

# comma seperated list of topics
# Default: 'frigate/available,frigate/events,frigate/stats'
# Debugging: 'frigate/+
# limited to 5 topics, all extras will be dropped.
MQTT_TOPICS='frigate/available,frigate/events,frigate/stats'

```
- Bring the stack up:
```
sudo docker-compose up -d
```
- After stack is up, issue the following command to bring up tailscale:
```
sudo docker-compose exec tailscale tailscale up --advertise-routes=192.168.200.0/24 --accept-routes
```
- Follow the Auth URL and either add to your existing account or create a new one.  Its free and easy to use.

- Configure Home Assistant Automation provide notifications:

### Home Assistant Automation
Home Assistant Automation adds a "break" using an input boolean helper.
```yaml
alias: fEVR Backyard Person Alert
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
      trigger.payload_json["after"]["camera"] == "backyard"
      }}
action:
  - choose:
      - conditions:
          - condition: state
            state: 'off'
            entity_id: input_boolean.fevrbackyardanimal
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
                    title: fEVR
                    uri: https://fevr.local:5080/?action=event&id={{trigger.payload_json['after']['id']}}
                image: >-
                  /api/frigate/notifications/{{trigger.payload_json['after']['id']}}/snapshot.jpg?bbox=1
                tag: '{{trigger.payload_json["after"]["id"]}}'
                alert_once: true
          - service: input_boolean.turn_on
            data: {}
            target:
              entity_id: input_boolean.fevrbackyardanimal
          - delay:
              hours: 0
              minutes: 0
              seconds: 30
              milliseconds: 0
          - service: input_boolean.turn_off
            data: {}
            target:
              entity_id: input_boolean.fevrbackyardperson
    default: []
mode: single

```
## Help!
If you have any issues, please reach out and [file an issue](https://github.com/BeardedTek-com/fEVR/issues) or [start a discussion](https://github.com/BeardedTek-com/fEVR/discussions).

I hope you find this useful!
