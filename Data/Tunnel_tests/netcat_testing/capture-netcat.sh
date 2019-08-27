#!/bin/bash
export DATADIR="$PWD/data"
export CAPTURETIME=`date +%Y-%m-%d_%H-%M-%S`
export SCENARIO="$1"
REPEAT="$2"

[ -z "$SCENARIO" ] && SCENARIO=1
[ -z "$REPEAT" ] && REPEAT=1


for ((i=1; i<=REPEAT; i++))
do
    echo "Repeat Nr " $i
    export REPNUM=$i
    # Start the containerised applications
    docker-compose up -d
    echo "Sleeping"
    sleep 1
    echo "Sending"
    docker exec -it $(sudo docker ps -aqf "name=netcat_testing_netcat-send_1") /usr/share/scripts/test2.sh
#    docker exec -it $(sudo docker ps -aqf "name=netcat_testing_netcat-send_1") /usr/share/scripts/test2.sh
    docker-compose down --remove-orphans -v
done
