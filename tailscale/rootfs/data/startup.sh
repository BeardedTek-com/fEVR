#!/bin/sh
# setup ip forwarding
echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf
sysctl -p /etc/sysctl.conf

#start tailscale
sleep 5
tailscale up --advertise-routes=192.168.204.0/24 --accept-routes 2> tailscale_output >&2
echo "#############################################"
echo ""
cat tailscale_output
echo ""
echo "#############################################"