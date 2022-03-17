# fEVR - frigate Event Video Recorder

fEVR works along side of [frigate](https://frigate.video) and [home assistant](https://www.home-assistant.io/) to collect video and snapshots of objects detected using your existing camera systems.

## Features
- Stores video independently of frigate
- Home Assistant generates notifications and makes a RESTful command to fEVR to grab data from frigate
- fEVR stores, sorts, and makes browsing frigate events a snap.

![fEVR Main](./docs/img/fevr-v0.4.png)

### Cloud Instances of fEVR
- I will be offering cloud instances of fEVR starting on March 31st.
- [Click here](https://github.com/sponsors/BeardedTek-com) for more details.
### Cloud BETA Testing
- If you would like to beta test this feature, please let me know by submitting an issue.

## Known Bugs
-  [HTMLDialogElement.showModal() does not work properly in Firefox < 98](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal#browser_compatibility)
- [See Issues for other known bugs.](https://github.com/BeardedTek-com/fEVR/issues)

## Requirements:
- [home assistant](https://home-assistant.io)
- [frigate](https://frigate.video)

## Install
The easiest and recommended method of install is docker-compose.
- Included is a container running tailscale to securely access fEVR.  This is not 100% necessary, but far more secure.

- Create .env file
```
cp template.env .env
```
- Edit .env file and
```
# Set Docker Bridge Network Variables
NETWORK_NAME=beardnet
NETWORK_SUBNET=192.168.200.0/24
NETWORK_GATEWAY=192.168.200.1


# Set Tailscale Container Variables
TAILSCALE_IP=192.168.200.3
TAILSCALE_IMAGE=ghcr.io/beardedtek-com/tailscale:main
TAILSCALE_CONTAINER_NAME=tailscale-devel
TAILSCALE_CONTEXT=./docker/tailscale/
TAILSCALE_DATA=./vol/tailscale/data
TAILSCALE_VAR_LIB=./vol/tailscale/var_lib
TAILSCALE_COMMAND=/opt/tailscale/tailscale


# Set fEVR Container Variables
FEVR_IP=192.168.200.2
FEVR_IMAGE=ghcr.io/beardedtek-com/fevr:main
FEVR_CONTAINER_NAME=fevr-devel
FEVR_CONTEXT=./docker/fEVR/
FEVR_DEBUG=true
FEVR_TITLE=Home
FRGIGATE_URL=http://192.168.2.240:5000


# OPTIONAL NAS Variables
NAS_IP=192.168.2.240
NAS_EVENTS=/export/fevr
NAS_DATA=/export/fevr_data

```
- Bring the stack up:
```
sudo docker-compose up -d
```
- After stack is up, issue the following command to bring up tailscale:
```
sudo docker-compose exec tailscale tailscale up --advertise-routes=192.168.100.0/24 --accept-routes
```
- Follow the Auth URL and either add to your existing account or create a new one.  Its free and easy to use.

```yml
version: '2.4'
services:
  tailscale:                                                          # Provides tailscale functionality for the stack
#    build:                                                           # By default it uses the 192.168.100.0/24 network
#      context: ${TAILSCALE_CONTEXT}                                  # Start tailscale once the container is up:
#      dockerfile: Dockerfile                                         # docker-compose exec tailscale tailscale up --advertise-routes=192.168.100/24 --accept-routes
                                                                      # This will provide you with the Authorization URL to sign into tailscale.
    image: ${TAILSCALE_IMAGE:-ghcr.io/beardedtek-com/tailscale:main}
    container_name: ${TAILSCALE_CONTAINER_NAME:-tailscale}
    restart: unless-stopped
    volumes:
      - ${TAILSCALE_DATA:-./vol/tailscale/data}:/data
      - ${TAILSCALE_VAR_LIB:-./vol/tailscale/var_lib}:/var/lib        # Required for tailscale

      - /dev/net/tun:/dev/net/tun                                     # Required for tailscale
    cap_add:
      - net_admin                                                     # Required for tailscale
      - sys_module                                                    # Required for tailscale
    environment:
      DOCKER_SUBNET: ${NETWORK_SUBNET:-192.168.200.0/24}
    networks:
      beardnet:
        ipv4_address: ${TAILSCALE_IP:-192.168.200.3}
    privileged: true
    command: ${TAILSCALE_COMMAND:-/opt/tailscale/tailscale}
  fevr:
#    build:
#      context: ${FEVR_CONTEXT}
#      dockerfile: Dockerfile
    image: ${FEVR_IMAGE:-ghcr.io/beardedtek-com/fevr:main}
    container_name: ${FEVR_CONTAINER_NAME:-fevr-devel}
    restart: unless-stopped
    environment:
      FRIGATE_URL: "${FRIGATE_URL:-http://frigate.local:5000}"
      FEVR_DEBUG: "${FRIGATE_DEBUG:-true}"
      FEVR_IP: 192.168.200.2
      FEVR_PORT: ${FEVR_PORT:-5080}
      FEVR_CONTAINER_NAME: ${FEVR_CONTAINER_NAME:-fevr}
    privileged: true
    networks:
      beardnet:
        ipv4_address: ${FEVR_IP:-192.168.200.2}
    volumes:
     #- ./vol/fevr/data/:/var/www/data                              # OPTIONAL: expose /var/www/data folder which contains the SQLite database and config.json files
     #- ./vol/fevr/events:/var/www/html/events                      # OPTIONAL: save events to a local folder
     - nfsevents:/var/www/html/events                               # OPTIONAL: save events to an NFS share
     - nfsdata:/var/www/data
     - ./vol/fevr/data:/data
     - ./vol/fevr/events:/events
networks:
  beardnet:                                                         # Network definition for our tailscale network
    driver: bridge
    ipam:
      config:
        - subnet: ${NETWORK_SUBNET:-192.168.200.0/24}
          gateway: ${NETWORK_GATEWAY:-192.168.200.1}

volumes:
  nfsevents:                                                        # VOLUME DEFINITION FOR NFS share
    driver_opts:
      type: "nfs"
      o: "addr=${NAS_IP},nfsvers=4"                                 # Make sure to change to your NFS server's address
      # o: "addr=<your_nas_ip>,rw,nfsvers=4"                        # SOME NFS SHARES REQUIRE THIS!!!
      device: ":${NAS_EVENTS}"
  nfsdata:                                                          # VOLUME DEFINITION FOR NFS share
    driver_opts:
      type: "nfs"
      o: "addr=${NAS_IP},nfsvers=4"                                 # Make sure to change to your NFS server's address
      # o: "addr=<your_nas_ip>,rw,nfsvers=4"                        # SOME NFS SHARES REQUIRE THIS!!!
      device: ":${NAS_DATA}"
```

- Configure Home Assistant Automation to feed fevr with data:

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

If you have any issues, please reach out and [file an issue](https://github.com/BeardedTek-com/fEVR/issues).

I hope you find this useful!
