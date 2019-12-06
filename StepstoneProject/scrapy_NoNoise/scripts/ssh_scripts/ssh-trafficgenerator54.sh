#!/bin/sh
HOST=$1
PORT=$2
USER="root"
PASS="root"
sshpass -p $PASS ssh -v -4 -o StrictHostKeyChecking=no -p $PORT $USER@$HOST << !
ls
sleep 63
pwd
sleep 1
sleep 1
exit
!
