#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.10"
FTP_SERVER="172.16.238.11"
FTP_CLIENT="172.16.238.12"
USER="root"
PASS="root"
# Check if necessary to scan host
#KNOWNHOSTFILE=~/.ssh/known_hosts
#if [ ! -f "$KNOWNHOSTFILE" ]; then
#    ssh-keyscan -H $SERVER $CLIENT $TUNNEL >> ~/.ssh/known_hosts
#fi

#Choose random file
#FILE=$(ls /dataToShare_CLIENT | sort -R | tail -1)
#echo $FILE
FILE="SampleJPGImage_2mbmb.jpg"
echo "SCANNING"
echo "TRANSFERRING " $FILE
#cp /dataToShare/$FILE /receive
#sshpass -p $PASS ssh -L 22:localhost:7778 root@$SERVER -f -N
#sshpass -p $PASS ssh -L 7777:localhost:7777 $USER@$TUNNEL sshpass -p $PASS ssh -L 22:localhost:7777 -N $USER@$SERVER
#sshpass -p $PASS ssh -4 -L 7777:localhost:7778 $USER@$TUNNEL -f -N
#sshpass -p $PASS ssh -4 -L 7777:localhost:22 -N $USER@$SERVER -f -N
#sshpass -p $PASS ssh -4 -L 7775:localhost:7776 $USER@$TUNNEL sshpass -p $PASS ssh -4 -L 7776:localhost:22 -N $USER@$SERVER -f
sshpass -p $PASS scp -4 -o StrictHostKeyChecking=no -P 7777 $USER@$CLIENT:/dataToShare/$FILE /receive
echo "DONE"

