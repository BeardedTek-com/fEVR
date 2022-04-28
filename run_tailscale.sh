#!/bin/sh
# Enable IP forwarding
rm -f /etc/sysctl.conf
touch /etc/sysctl.conf
echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf 2> /dev/null
echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf 2> /dev/null
sysctl -p /etc/sysctl.conf

# Start tailscaled
tailscaled &

# While loop to make sure tailscaled has started
tailscale_status=""
OK=1
while [ $OK != 0 ]; do
    if ps ef | grep tailscaled | > /tmp/test.txt; then OK=0; else OK=1; fi
done


tailscale up --authkey="$AUTH_KEY" --accept-routes --advertise-routes="$BRIDGE_SUBNET" --accept-dns --hostname fevrflask
TS=0
while [ $TS == 0 ]; do
    sleep 10000
done