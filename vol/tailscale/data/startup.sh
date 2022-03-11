#!/bin/sh
#start tailscale
tailscale up --advertise-routes=192.168.204.0/24 --accept-routes 2> auth_url >&2
sleep 5
echo "#############################################"
echo ""
cat tailscale_output
echo ""
echo "#############################################"