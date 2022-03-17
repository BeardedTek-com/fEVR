FROM ghcr.io/home-assistant/amd64-base:3.14

# install apache2, python3, nano because, well, nano, and fevr's python requirements
RUN apk --no-cache add apache2 libxml2-dev apache2-utils py3-pip py3-pillow git bash nano rsync &&\
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip install pytz && \
    pip install python-dateutil && \
    pip install requests && \
    pip install sqlite_web && \
    rm -rf /var/www/logs

# Copy root filesystem
COPY rootfs /

# get latest version of fEVR, enable CGI Environment, set permissions, and cleanup files
RUN chmod +x /opt/fevr/setup/enable_cgi && /opt/fevr/setup/enable_cgi \
 && chown -R 100:1000 /var/www \
 && chmod -R 0770 /var/www \
 && chmod -R 0770 /opt/fevr \
 && chown root:101 /opt/fevr/setup/dbsetperms \
 && chmod u+s /opt/fevr/setup/dbsetperms
