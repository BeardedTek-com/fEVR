FROM docker.beardedtek.com/beardedtek-com/fevr-base:latest
COPY . /fevr
COPY rootfs /
RUN chown -R fevr /fevr
WORKDIR /fevr
EXPOSE 5090
