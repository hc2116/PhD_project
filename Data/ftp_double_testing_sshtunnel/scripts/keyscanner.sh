#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.10"
FTP_SERVER="172.16.238.11"
#LOCALHOST="[localhost]:7777"
# Check if necessary to scan host
KNOWNHOSTFILE=~/.ssh/known_hosts
ssh-keyscan -H $SERVER $CLIENT $TUNNEL $FTP_SERVER >> ~/.ssh/known_hosts
