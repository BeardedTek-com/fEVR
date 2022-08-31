# Notifications

## More coming in 0.7
In the next major version, I am introducing notifications through [ntfy.sh](https://ntfy.sh) and [apprise](https://github.com/caronc/apprise-api).

Apprise has the capability to send notifications on over 80 different platforms including Home Assistant.

## Home Asisstant 
### ***Depricated***
### While this was a usable procedure when originally written, I don't plan on providing support, help, or developing this further
As noted above, notifications are coming in 0.7 using ntfy.sh and apprise.  Home Assistant is changing way too fast to keep up with all the cool new ways to do things.  Feel free to try this method, but no guarantees.

---

Honestly, this is a bit of a pain in the rear. For each notification type you want for each camera, a helper entity must be added.
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
`<<CAMERA>>` is the camera name
`<<HELPER ENTITY>>` is the entity you created for this notification
`<<YOUR FEVR URL>>` is the url to your fevr instance

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
