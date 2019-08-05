#!/bin/sh

USER="$1"
PASS="$2"


#!/bin/sh

USR="testuser1"
PW="testpassword123"
useradd $USR
echo "user $USR added successfully!"
echo $USR:$PW | chpasswd
echo "Password for user $USR changed successfully"





#Choose random file
export FILE=$(ls /dataToShare | sort -R | tail -1)
echo $FILE

echo "WAITING FOR TCPDUMP TO LAUNCH"
sleep 20
echo "SCANNING"
#mkdir ~/.ssh
#ssh-keyscan -H $HOST $HOST2 >> ~/.ssh/known_hosts
#ssh-keyscan -H  >> ~/.ssh/known_hosts
echo "TRANSFERRING " $FILE
#sshpass -p $PASS scp $USER@$HOST:/dataToShare/$FILE /receive
sshpass -p $PASS scp $USER@$HOST2:/dataToShare/$FILE /receive

#sshpass -p $PASS ssh -L $USER@$HOST 22:$HOST2:22 -f -N
#sshpass -p $PASS ssh -L $USER@$HOST2 22:$HOST:22 -f -N
#sshpass -p $PASS ssh $USER@$HOST "sleep 5; ls;sleep 5; ls; sleep5; ls"
echo "DONE"

