#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL1="172.16.238.10"
TUNNEL2="172.16.238.9"
FTP_SERVER="172.16.238.11"
FTP_CLIENT="172.16.238.12"
NETCAT_SERVER="172.16.238.18"
USER="root"
PASS="root"


echo "Creating client-tunnel "

sshpass -p $PASS ssh -4 -o StrictHostKeyChecking=no -L \*:21:$TUNNEL1:7777 -L \*:20:$TUNNEL1:7778 -L \*:18:$NETCAT_SERVER:18 -L \*:19:$NETCAT_SERVER:19 root@$TUNNEL2 -f -N

#sshpass -p $PASS ssh -4 -o StrictHostKeyChecking=no -L \*:21:$TUNNEL1:7777 root@$TUNNEL2 -f -N


echo "DONE"

