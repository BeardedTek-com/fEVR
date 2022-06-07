FROM ghcr.io/home-assistant/amd64-base-python:3.10-alpine3.15
COPY . /fevr
COPY rootfs /
WORKDIR /fevr
RUN apk --no-cache add py3-pip pcre pcre2 git nano tailscale caddy \
                       python3-dev build-base linux-headers pcre-dev &&\
    ln -s /usr/bin/python3 /usr/bin/python && \
    python3 -m pip install -r requirements.txt && \
    apk --no-cache del python3-dev build-base linux-headers pcre-dev && \
    mkdir /data && \
    ln -s /fevr/app/static/events /data/events && \
    adduser -u 1000 -h /fevr -D fevr && \
    chown -R fevr /fevr && \
    chown -R fevr /data