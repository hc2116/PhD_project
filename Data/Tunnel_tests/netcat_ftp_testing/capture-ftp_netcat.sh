#!/bin/bash

export SCENARIO="$1"
REPEAT="$2"
DURATION="$3"
export CAPTURETIME=`date +%Y-%m-%d_%H-%M-%S`
export DATADIR="$PWD/data"

[ -z "$REPEAT" ] && REPEAT=1
[ -z "$SCENARIO" ] && SCENARIO=1
[ -z "$DURATION" ] && DURATION=60

function bringup {
    echo "Start the containerised applications..."
    #export DATADIR="$PWD/data"
    docker-compose --no-ansi --log-level ERROR up -d
}

function teardown {
    echo "Take down the containerised applications and networks..."
    # NB: this removes everything so it is hard to debug from this script
    # TODO: add a `--debug` option instead use `docker-compose stop`.
    docker-compose --no-ansi --log-level ERROR down --remove-orphans -v
    echo "Done."
}

trap '{ echo "Interrupted."; teardown; exit 1; }' INT
#trap '{ echo "EXITED."; teardown; exit 0; }' EXIT

for ((i=1; i<=REPEAT; i++))
do
    echo "Repeat Nr " $i
    # Randomise user-ID and password
    RN=$((1 + RANDOM % 200))
    Pi=`echo "4*a(1)" | bc -l`
    RN2=$(echo "1000*(s((0.5*$RN/32767)*$Pi)/c((0.5*$RN/32767)*$Pi))" | bc -l)
    RN3=$(echo "5+(2*$RN2+1)/2" | bc )
    export User=$(cat /dev/urandom | tr -dc 'a-z' | fold -w $RN3 | head -n 1)
    echo "User " $User
    ################
    RNP=$((1 + RANDOM % 200))
    RNP2=$(echo "1000*(s((0.5*$RNP/32767)*$Pi)/c((0.5*$RNP/32767)*$Pi))" | bc -l)
    RNP3=$(echo "5+(2*$RNP2+1)/2" | bc )
    export Password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $RNP3 | head -n 1)	
    echo "Password " $Password
    ################

    rm -f -r users
    mkdir users
    mkdir users/"$User"
    cp -r  dataToShare/* users/"$User"/
    rm -f $PWD/receive/*
    rm -f $PWD/receive_SERVER/*
    export REPNUM=$i
    bringup;
    echo "WAITING FOR TCPDUMP TO LAUNCH"
    $PWD/scripts/container_filter.sh netcat_ftp_testing_ftp_server_1 sport 60000
    sleep 5
    echo "Sending"
    sleep $DURATION
    docker exec -d -it $(sudo docker ps -aqf "name=netcat_ftp_testing_netcat-send_1") /usr/share/scripts/test2.sh
    docker exec -ti $(sudo docker ps -aqf "name=netcat_ftp_testing_ftp_client_1") /usr/src/scripts/inclient1.sh $User $Password 
    teardown;

    rm -f -r users

done