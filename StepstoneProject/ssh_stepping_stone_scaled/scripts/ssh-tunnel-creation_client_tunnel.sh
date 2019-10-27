#!/bin/sh
STARTPOINT_IP=$1
ENDPOINT_IP=$2
RELAY_IP=$3
ENTRY_PORT=$4

USER="root"
PASS="root"


echo "Creating startpoint-tunnel "
NETCAT_SERVER_IP=localhost

sshpass -p $PASS ssh -4 -o StrictHostKeyChecking=no -L \*:$ENTRY_PORT:localhost:7777 -L \*:18:$NETCAT_SERVER_IP:18 -L \*:19:$NETCAT_SERVER_IP:19 root@$RELAY_IP -f -N


echo "DONE"

