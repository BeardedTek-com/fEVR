FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
COPY . /fevr
RUN addgroup -S fevr -g 1000 && adduser -S fevr -G fevr -u 1000 && \
    apk --no-cache add py3-pip py3-pillow py3-paho-mqtt py3-requests py3-dotenv git && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    git clone https://github.com/beardedtek-com/fevr
COPY rootfs /
RUN chown -R 1000:1000 /fevr
WORKDIR /fevr