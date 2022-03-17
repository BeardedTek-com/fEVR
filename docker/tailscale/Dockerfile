FROM crazymax/alpine-s6:3.15-edge
COPY rootfs /

# Install Tailscale
# Set permissions for /etc/services.d folder
# enable ipv4 forwarding
# enable ipv6 forwarding
# save changes with sysctl
RUN apk --no-cache add tailscale \
 && chmod -R 0770 /etc/services.d/* \
 && echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf \
 && echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf \
 && sysctl -p /etc/sysctl.conf

# Start tailscaled
CMD /opt/tailscale/tailscale
ENTRYPOINT tailscaled