#!/bin/sh
HOST="172.16.238.5"
USER="root"
PASS="root1"
#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE

echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 20
echo "SCANNING"
mkdir ~/.ssh
ssh-keyscan -H $HOST >> ~/.ssh/known_hosts
echo "TRANSFERRING " $FILE
sshpass -p $PASS scp $USER@$HOST:/dataToShare/$FILE /receive
echo "DONE"

