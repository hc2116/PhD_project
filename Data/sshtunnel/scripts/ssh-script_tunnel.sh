#!/bin/sh
HOST="172.16.238.5"
HOST2="172.16.238.10"
HOST3="172.16.238.15"
USER="root"
PASS="root"
#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE

echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 20
echo "SCANNING"
#mkdir ~/.ssh
#ssh-keyscan -H $HOST $HOST2 $HOST3 >> ~/.ssh/known_hosts
echo "TRANSFERRING " $FILE
#sshpass -p $PASS scp $USER@$HOST:/dataToShare/$FILE /receive
#sshpass -p $PASS scp $USER@$HOST2:/dataToShare/$FILE /receive
#sshpass -p $PASS ssh $USER@$HOST2 "sshpass -p $PASS ssh -L $USER@$HOST3 22:$HOST:22 -f -N"

#sshpass -p $PASS ssh -L $USER@$HOST3 22:$HOST:22 -f -N
sshpass -p $PASS ssh -L $USER@$HOST2 1223:$HOST:22
#sshpass -p $PASS scp $USER@$HOST2:/dataToShare/$FILE /receive
#sshpass -p $PASS ssh -L $USER@$HOST2 22:$HOST:22 -f -N
#sshpass -p $PASS ssh $USER@$HOST "sleep 5; ls;sleep 5; ls; sleep5; ls"
echo "DONE"

