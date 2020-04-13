#!/bin/bash

REPEAT=$1
DURATION=$2
DURATION2=$3
export PROJECT_NAME=$4
export IP_RANGE=$5
export CAPTURETIME=`date +%Y-%m-%d_%H-%M-%S`
export DATADIR="$PWD/data"
export SCENARIO=1

[ -z "$REPEAT" ] && REPEAT=1
[ -z "$DURATION" ] && DURATION=2
[ -z "$DURATION2" ] && DURATION2="40s"
[ -z "$PROJECT_NAME" ] && PROJECT_NAME="ssh_stepping_stone_scaled"
[ -z "$IP_RANGE" ] && IP_RANGE=16

export SCRAPY_IP="172.${IP_RANGE}.238.2"
export STARTPOINT_IP="172.${IP_RANGE}.238.7"
export RELAY_IP="172.${IP_RANGE}.238.8"
export ENDPOINT_IP="172.${IP_RANGE}.238.9"
export SSH_SERVER_IP="172.${IP_RANGE}.238.1" #localhost
export SSH_CLIENT_IP=localhost

ENTRY_PORT=7777
OUTWARD_PORT=3128

NETCAT_PARA1=0.1
NETCAT_PARA2=10000
NETCAT_PARA3=10
NETCAT_PARA4=0.1
NETCAT_PARA5=10000
NETCAT_PARA6=10

DELAY_PARA1=6
DELAY_PARA2=1
DELAY_PARA3=1000
DELAY_PARA4=20




function bringup {
    echo "Start the containerised applications..."
    #export DATADIR="$PWD/data"
    docker-compose -p ${PROJECT_NAME} --no-ansi --log-level ERROR up -d
}

function teardown {
    echo "Take down the containerised applications and networks..."
    # NB: this removes everything so it is hard to debug from this script
    # TODO: add a `--debug` option instead use `docker-compose stop`.
    docker-compose  -p ${PROJECT_NAME} --no-ansi --log-level ERROR down --remove-orphans -v
    echo "Done."
}

trap '{ echo "Interrupted."; teardown; exit 1; }' INT


for ((i=1; i<=REPEAT; i++))
do
    echo "Repeat Nr " $i
    export REPNUM=$i
    rm -f $PWD/scripts/localhost-*
#    rm -f $PWD/receive/*
#    rm -r -f dataToShare_server

    rm -f scrapy/spider_${PROJECT_NAME}.py
    cp scrapy/spider_backup/spider.py scrapy/spider_${PROJECT_NAME}.py
    sudo chmod 777 scrapy/spider_${PROJECT_NAME}.py
    
    #sed -i "s/PLACEHOLDERURL/${IP_RANGE}/g" scrapy/spider_${PROJECT_NAME}.py

    IFS=',' 
    URL=$(shuf -n 1 ../top-1m.csv)
    read -a URL <<< "$URL"
    sed -i "s/PLACEHOLDER1/${URL[1]}/g" scrapy/spider_${PROJECT_NAME}.py

    URL=$(shuf -n 1 ../top-1m.csv)
    read -a URL <<< "$URL"
    sed -i "s/PLACEHOLDER2/${URL[1]}/g" scrapy/spider_${PROJECT_NAME}.py

    URL=$(shuf -n 1 ../top-1m.csv)
    read -a URL <<< "$URL"
    sed -i "s/PLACEHOLDER3/${URL[1]}/g" scrapy/spider_${PROJECT_NAME}.py
    bringup;
    echo "WAITING FOR TCPDUMP TO LAUNCH"
    sleep 2
    ###########################################################################################
    echo "Creating tunnels in $DURATION seconds...."
    sleep $DURATION
    timeout -k $(($DURATION2+2)) $DURATION2 docker exec -ti $(sudo docker ps -aqf "name=${PROJECT_NAME}_spider_1") scrapy runspider "scrapy/spider_${PROJECT_NAME}.py"; EXIT_CODE=$?
    sleep 1
    teardown
    echo $EXIT_CODE
done