FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
COPY . /fevr
COPY rootfs /
RUN apk --no-cache add py3-pip py3-pillow py3-paho-mqtt py3-requests py3-dotenv git nano tailscale
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN adduser -u 1000 -h /fevr -D fevr
WORKDIR /fevr

# FEVR ENV Variables
ENV FEVR_PORT=5090
ENV FLASK_ENV=development

# MQTT ENV Variables
ENV MQTT_BROKER_IP=127.0.0.1
ENV MQTT_BROKER_PORT=1883
ENV MQTT_BROKER_USER=
ENV MQTT_BROKER_PASS=
ENV MQTT_TOPICS=frigate/+

# TAILSCALE ENV Variables
ENV TAILSCALE_ENABLE=false
ENV TAILSCALE_TAGS=tag:fevr
ENV TAILSCALE_HOSTNAME=fevr
ENV TAILSCALE_AUTHKEY=