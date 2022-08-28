# Installation

## Docker Compose:
docker-compose is the preferred installation method
## Create directory structure
```
mkdir fevr
cd fevr
mkdir data
mkdir events
```

### Create .env file
A template .env file is available [on GitHub](https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/template.env) and down below:
NOTE: The IP addresses in the .env file are for internal bridge networking and SHOULD NOT be on the same subnet as your home network.
The default values should serve you well.

```
curl -o .env https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/template.env
nano .env
```
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
### Edit docker-compose.yml
A template docker.compose.yml file is provided [on GitHub](https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/docker-compose.yml) and down below:

```
cd ..
curl -o docker-compose.yml https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/docker-compose.yml
nano docker-compose.yml
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
**config.yml should be placed in the defined volume for `data` listed in the docker-compose.yml file provided.**

More Information on mqtt_client is available [here](https://ghost.fevr.video/mqtt-client)

An example config.yml is provided [on GitHub](https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/config.yml.template) and below
```
cd data
wget -o config.yml https://raw.githubusercontent.com/BeardedTek-com/fEVR/main/config.yml.template
nano config.yml
```
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
```
cd ..
```

## Bring the system up:
```
docker-compose up -d
```