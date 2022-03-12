#!/bin/sh

# enable ip forwarding
echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf 2> /dev/null
echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf 2> /dev/null
sysctl -p /etc/sysctl.conf

# start tailscale
tailscale up --advertise-routes=192.168.204.0/24 --accept-routes 2> /tmp/auth &
sleep 3
authURL="$(cat /tmp/auth | grep http | sed 's/^[ \t]*//')"
echo "#############################################"
echo ""
echo "Tailscale Authorization URL: $authURL"
echo ""
echo "#############################################"
n=0
while true
do
    sleep 300
done