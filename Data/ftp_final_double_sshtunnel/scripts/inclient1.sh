#!/bin/sh
HOST="172.16.238.20"
USER="$1"
PASS="$2"
FILE=$(ls /dataToShare/ | sort -R | tail -1)

echo "CONNECTING ..."
ftp -n $HOST <<END_SCRIPT
pass
quote USER $USER
quote PASS $PASS
pwd
ls
verbose
bin
quit
END_SCRIPT
exit 0
