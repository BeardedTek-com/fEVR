FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
COPY . /fevr
COPY rootfs /
RUN apk --no-cache add py3-pip py3-pillow py3-paho-mqtt py3-requests py3-dotenv git nano tailscale uwsgi
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN mkdir /data
RUN ln -s /fevr/app/static/events /data/events
RUN adduser -u 1000 -h /fevr -D fevr
RUN chown -R fevr /fevr
RUN chown -R fevr /data
WORKDIR /fevr