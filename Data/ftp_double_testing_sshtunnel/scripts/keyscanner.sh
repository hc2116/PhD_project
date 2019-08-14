#!/bin/sh
SERVER="172.16.238.5"
CLIENT="172.16.238.20"
TUNNEL="172.16.238.10"
#LOCALHOST="[localhost]:7777"
# Check if necessary to scan host
KNOWNHOSTFILE=~/.ssh/known_hosts
ssh-keyscan -H $SERVER $CLIENT $TUNNEL >> ~/.ssh/known_hosts
