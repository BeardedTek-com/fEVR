#!/bin/sh
# setup ip forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf

#start tailscale
tailscale up --advertise-routes=192.168.2.204.0/24 --accept-routes