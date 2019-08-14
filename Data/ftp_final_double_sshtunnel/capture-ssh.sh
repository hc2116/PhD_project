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

function keyscanning {
    #rm -f $PWD/.ssh_client/known_hosts
    #rm -f $PWD/.ssh_test_client/known_hosts
    #rm -f $PWD/.ssh_tunnel/known_hosts
    #rm -f $PWD/.ssh_server/known_hosts
    KNOWNHOSTFILE=$PWD/.ssh_client/known_hosts
    if [ ! -f "$KNOWNHOSTFILE" ]; then
        echo "Client scanning Hosts"
        docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_client_1") /scripts/keyscanner.sh
    fi
    KNOWNHOSTFILE=$PWD/.ssh_test_client/known_hosts
    if [ ! -f "$KNOWNHOSTFILE" ]; then
        echo "Client scanning Hosts"
        docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_test_client_1") /scripts/keyscanner.sh
    fi
    KNOWNHOSTFILE=$PWD/.ssh_tunnel/known_hosts
    if [ ! -f "$KNOWNHOSTFILE" ]; then
        echo "Tunnel scanning Hosts"
        docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_tunnel_1_1") /scripts/keyscanner.sh
    fi
    KNOWNHOSTFILE=$PWD/.ssh_server/known_hosts
    if [ ! -f "$KNOWNHOSTFILE" ]; then
        echo "Server scanning Hosts"
        docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_server_1") /scripts/keyscanner.sh
    fi

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
    sleep 5
    echo "Capturing data now for $DURATION seconds...."
    keyscanning;
    docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_client_1") /scripts/ssh-tunnel-creation_client_tunnel.sh
    docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_tunnel_1_1") /scripts/ssh-tunnel-creation_tunnel_server.sh
    docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_test_client_1") /scripts/ssh-tunnel-sending.sh

    sleep $DURATION
    teardown;

    rm -f -r users
    rm -f $PWD/receive/*
    rm -f $PWD/receive_SERVER/*

done
