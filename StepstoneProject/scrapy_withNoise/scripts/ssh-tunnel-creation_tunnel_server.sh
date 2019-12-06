#!/bin/sh
STARTPOINT_IP=$1
ENDPOINT_IP=$2
RELAY_IP=$3
OUTWARD_PORT=$4
SSH_SERVER_IP=$5
NETCAT_SERVER_IP=localhost


USER="root"
PASS="root"


echo "Creating endpoint-tunnel"
sshpass -p $PASS ssh -4 -o StrictHostKeyChecking=no -L \*:7777:$SSH_SERVER_IP:$OUTWARD_PORT -L \*:16:$NETCAT_SERVER_IP:16 -L \*:17:$NETCAT_SERVER_IP:17 root@$ENDPOINT_IP -f -N

echo "DONE"

