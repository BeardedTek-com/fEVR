FROM docker.beardedtek.com/beardedtek/fevr-base:0.6.0
COPY . /fevr
COPY rootfs /
WORKDIR /fevr
RUN chown -R fevr /fevr && \
    apk --no-cache add python3-dev build-base linux-headers pcre-dev &&\
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install wheel && \
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    apk --no-cache del python3-dev build-base linux-headers pcre-dev
