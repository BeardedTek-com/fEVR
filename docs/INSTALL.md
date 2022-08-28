# Installation

## Docker Compose:
docker-compose is the preferred installation method

### Environment Variables **NOT RECOMMENDED**
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
      - ./events:/fevr/app/static/events
      - ./data:/fevr/app/data
      - ./varlib:/var/lib
    environment:
      FEVR_DEVELOPMENT: ${FEVR_DEVELOPMENT:-false}
      TAILSCALE_ENABLE: ${TAILSCALE_ENABLE:-false}
      TAILSCALE_AUTHKEY: ${TAILSCALE_AUTHKEY}
      TAILSCALE_HOSTNAME: ${TAILSCALE_HOSTNAME:-fevr}
      TAILSCALE_TAGS: ${TAILSCALE_TAGS}
```

### Create config.yml for mqtt_client
This config.yml is separate from fEVR as mqtt_client can run separately from fEVR.
In most use cases, running inside the docker container will be sufficient.
At least 1 mqtt_client instance needs to be running either in the docker container or on a separate host as long as it can communicate with the main fEVR instance.

More Information on mqtt_client is available in [docs/MQTT_CLIENT.md](MQTT_CLIENT)

An example config.yml is provided [config.yml.template](../config.yml.template) and below
```
fevr_host: localhost
fevr_port: 5090
fevr_transport: http://
mqtt_broker: mqtt
mqtt_port: 1883
mqtt_user: ~
mqtt_password: ~
mqtt_topics:
    - frigate/available
    - frigate/events
    - frigate/stats
mqtt_apikey: 128-bit-apikey-from-fevr
verbose: true
```
config.yml should be placed in the defined volume for `data` listed in the docker-compose.yml file provided.

## Bring the system up:
```
docker-compose up -d
```