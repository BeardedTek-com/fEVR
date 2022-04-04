# Requirements:

- [docker](https://docker.com)
- [docker-compose](https://docs.docker.com/compose/)
- [Home Assistant](https://home-assistant.io)
- [frigate](https://frigate.video)


# Installation

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