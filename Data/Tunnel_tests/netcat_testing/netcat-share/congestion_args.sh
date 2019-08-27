#!/bin/sh

IP="$1"

function congest {
	cat /dev/random | nc $IP 2222
}

sleep 1
#read_bytes;
#touch /usr/share/scripts/test2.txt
congest;

