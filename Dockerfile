FROM ghcr.io/home-assistant/amd64-base:3.14

# install apache2, python3, nano because, well, nano, and fevr's python requirements
RUN apk --no-cache add apache2 libxml2-dev apache2-utils py3-pip py3-pillow git bash nano &&\
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip install pytz && \
    pip install python-dateutil && \
    pip install requests && \
    pip install sqlite_web && \
    rm -rf /var/www/logs

# Copy root filesystem
COPY rootfs /

# get latest version of fEVR, enable CGI Environment, set permissions, and cleanup files
RUN git clone https://github.com/beardedtek-com/fevr && mv fevr/app/* /var/www/ \
 && mkdir /var/www/logs && touch /var/www/logs/debug.log \
 && mv /var/www/db/fEVR.blank.sqlite /var/www/db/fEVR.sqlite \
 && mv /var/www/config/config-example.json /var/www/config/config.json \
 && bash /enable_cgi.sh \
 && chown -R 100:101 /var/www \
 && chmod -R 0770 /var/www \
 && chmod +x /writeConfig \
  && rm -rf /fevr
