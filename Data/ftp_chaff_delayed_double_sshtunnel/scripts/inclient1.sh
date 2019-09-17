#!/bin/sh
HOST="172.16.238.20"
USER="$1"
PASS="$2"

FILE=$(ls /dataToShare/ | sort -R | tail -1)
echo "CONNECTING ..."
ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASS
pwd
verbose
ls
bin
get $FILE
delete $FILE
quit
END_SCRIPT
exit 0
