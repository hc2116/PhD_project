#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.10"
FTP_SERVER="172.16.238.11"
FTP_CLIENT="172.16.238.12"
USER="root"
PASS="root"
# Check if necessary to scan host
KNOWNHOSTFILE=~/.ssh/known_hosts
if [ ! -f "$KNOWNHOSTFILE" ]; then
    ssh-keyscan -H $SERVER $CLIENT $TUNNEL >> ~/.ssh/known_hosts
fi

echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 5
echo "Creating tunnel "

sshpass -p $PASS ssh -4 -L 7777:$FTP_SERVER:21 root@$SERVER  -f -N
sshpass -p $PASS ssh -4 -R \*:21:localhost:7777 root@$CLIENT -f -N

#sshpass -p $PASS ssh -4 -L 7777:localhost:22 root@$SERVER -f -N
#sshpass -p $PASS ssh -4 -R 7777:localhost:7777 root@$CLIENT -f -N
echo "SLEEPING"
sleep 15
echo "DONE"

