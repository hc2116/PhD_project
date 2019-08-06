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

#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE
echo "SCANNING"
echo "TRANSFERRING " $FILE
#cp /dataToShare/$FILE /receive
#sshpass -p $PASS ssh -L 22:localhost:7778 root@$SERVER -f -N
#sshpass -p $PASS ssh -L 7777:localhost:7777 $USER@$TUNNEL sshpass -p $PASS ssh -L 22:localhost:7777 -N $USER@$SERVER
sshpass -p $PASS scp -P 7777 $USER@localhost:/dataToShare/$FILE /receive
echo "DONE"

