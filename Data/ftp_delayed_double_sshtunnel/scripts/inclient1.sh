#!/bin/sh
HOST="172.16.238.20"
USER="$1"
PASS="$2"

echo "CONNECTING ..."
ftp -n $HOST <<END_SCRIPT
pass
quote USER $USER
quote PASS $PASS
pwd
ls
quit
END_SCRIPT
exit 0
