#!/bin/sh
HOST=$1
PORT=$2
USER="root"
PASS="root"

#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE

echo "TRANSFERRING " $FILE
sshpass -p $PASS scp -v -4 -o StrictHostKeyChecking=no -P $PORT $USER@$HOST:/dataToShare/$FILE /receive

echo "DONE"

