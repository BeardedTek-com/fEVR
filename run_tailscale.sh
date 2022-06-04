#!/bin/sh
echo "$USE_TAILSCALE"
if [ "$USE_TAILSCALE" != "false" ]; then
    echo "##### TAILSCALE ENABLED #####"
    # Enable IP forwarding
    rm -f /etc/sysctl.conf
    touch /etc/sysctl.conf
    echo 'net.ipv4.ip_forward = 1' | tee -a /etc/sysctl.conf 2> /dev/null
    echo 'net.ipv6.conf.all.forwarding = 1' | tee -a /etc/sysctl.conf 2> /dev/null
    sysctl -p /etc/sysctl.conf

    # Start tailscaled
    apk add tailscale
    echo "##### STARTING TAILSCALED #####"
    tailscaled &

    # While loop to make sure tailscaled has started
    tailscale_status=""
    OK=1
    while [ $OK != 0 ]; do
        if ps ef | grep tailscaled | > /tmp/test.txt; then OK=0; else OK=1; fi
    done

    echo "##### BRINGING UP TAILSCALE #####"
    echo "##### tags: $TAILSCALE_TAGS"
    echo "##### hostname: $TAILSCALE_HOSTNAME"
    echo "##### auth_key: $AUTH_KEY"
    tailscale up --authkey="$AUTH_KEY" --accept-routes --accept-dns --hostname "$TAILSCALE_HOSTNAME" --advertise-tags=$TAILSCALE_TAGS
    TS=0
    while [ $TS == 0 ]; do
        sleep 5000
    done
else
    echo "##### TAILSCALE DISABLED #####"
fi