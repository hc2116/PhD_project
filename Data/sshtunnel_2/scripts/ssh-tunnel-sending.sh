#!/bin/sh
echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 30
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.20"
USER="root"
PASS="root"
# Check if necessary to scan host
KNOWNHOSTFILE=~/.ssh/known_hosts
if [ ! -f "$KNOWNHOSTFILE" ]; then
    ssh-keyscan -H $SERVER $CLIENT $TUNNEL >> ~/.ssh/known_hosts
fi

#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE
echo "SCANNING"
echo "TRANSFERRING " $FILE
#cp /dataToShare/$FILE /receive
sshpass -p $PASS scp -P 7777 $USER@localhost:/dataToShare/$FILE /receive
echo "DONE"

