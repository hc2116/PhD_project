#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.10"
USER="root"
PASS="root"
# Check if necessary to scan host
KNOWNHOSTFILE=~/.ssh/known_hosts
if [ ! -f "$KNOWNHOSTFILE" ]; then
    ssh-keyscan -H $SERVER $CLIENT $TUNNEL >> ~/.ssh/known_hosts
fi

echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 20
echo "Creating tunnel "
sshpass -p $PASS ssh -R 7777:$SERVER:22 root@$CLIENT -f -N
sleep 100
echo "DONE"

