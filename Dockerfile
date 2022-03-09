FROM ghcr.io/home-assistant/amd64-base:3.14

RUN apk --no-cache add apache2 libxml2-dev apache2-utils py3-pip py3-pillow git bash nano nfs-utils
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install python dependencies
RUN pip install pytz && \
    pip install python-dateutil && \
    pip install requests && \
    pip install sqlite_web

# get rid of symlink /var/www/logs
RUN rm -f /var/www/logs

# Copy root filesystem
COPY rootfs /

# get latest version of fEVR
RUN git clone -b v0.3.4 https://github.com/beardedtek-com/fevr && mv fevr/app/* /var/www/ \
 && mkdir /var/www/logs && touch /var/www/logs/debug.log \
 && mv /var/www/db/fEVR.blank.sqlite /var/www/db/fEVR.sqlite \
 && mv /var/www/config/config-example.json /var/www/config/config.json

# Setup CGI Environment & Set Permissions
RUN bash /enable_cgi.sh \
 && chown -R 100:101 /var/www \
 && chmod -R 0770 /var/www \
 && chmod +x /writeConfig

 # Cleanup
 RUN rm -rf /fevr