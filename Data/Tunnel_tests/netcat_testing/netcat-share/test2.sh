#!/bin/sh
#ls
echo "hello Henry"
while true
do
    #echo "hello Henry" | nc -u -p 1234 172.16.238.15 8888
    sleep 0.1
    echo "hello Henry"
done | nc -u -p 1234 172.16.238.15 8888
sleep 2

