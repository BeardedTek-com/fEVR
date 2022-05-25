FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
COPY . /fevr
RUN apk --no-cache add py3-pip py3-pillow py3-paho-mqtt py3-requests py3-dotenv git && \
    ln -s /usr/bin/python3 /usr/bin/python
COPY rootfs /
RUN chown -R 1000:1000 /fevr
WORKDIR /fevr