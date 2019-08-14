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
    rm -f $PWD/.ssh_client/known_hosts
    rm -f $PWD/.ssh_tunnel/known_hosts
    rm -f $PWD/.ssh_server/known_hosts
    KNOWNHOSTFILE=$PWD/.ssh_client/known_hosts
    if [ ! -f "$KNOWNHOSTFILE" ]; then
        echo "Client scanning Hosts"
        docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_client_1") /scripts/keyscanner.sh
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
#    echo "Scenario" $SCENARIO
    rm -f $PWD/receive/*
    rm -f $PWD/receive_SERVER/*
    export REPNUM=$i
    bringup;
    echo "WAITING FOR TCPDUMP TO LAUNCH"
    sleep 10
    echo "Capturing data now for $DURATION seconds...."
    keyscanning;
    docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_tunnel_1_1") /scripts/ssh-tunnel-creation.sh
    docker exec -it $(sudo docker ps -aqf "name=sshtunnel_ssh_client_1") /scripts/ssh-tunnel-sending.sh
    sleep $DURATION
    teardown;
done
