#!/bin/sh
#ls
echo "hello world"
IP=$1
PORT=$2
RANGE=$3

#mkfifo udp2tcp
#netcat -l 172.16.238.13 21 < /tmp/tcp2udp | netcat -u localhost 9200 > /tmp/tcp2udp
#nc -l 9200 > /usr/share/scripts/test3.txt
nc -l $IP $PORT > "/usr/share/scripts/$IP-$PORT-$RANGE.txt"

sleep 2
