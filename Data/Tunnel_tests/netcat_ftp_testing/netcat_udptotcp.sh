#!/bin/sh
DEST=$1
PORT1=$2
PORT2=$3

mkfifo udp2tcp
nc -l -u -p 9100 < udp2tcp | nc -p $PORT2 $DEST $PORT1  > udp2tcp

