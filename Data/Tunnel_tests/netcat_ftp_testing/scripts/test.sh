#!/bin/sh
#ls
echo "hello world"
#echo "hello world" > /usr/share/scripts/test.txt
nc -l -u 172.16.238.13 8888 > /usr/share/scripts/test3.txt
sleep 2
