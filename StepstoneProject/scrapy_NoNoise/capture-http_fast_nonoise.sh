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

export REPNUM=1
bringup;

echo "Creating tunnels...."
#sleep $DURATION
docker exec -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_relay_startpoint_1") /scripts/ssh-tunnel-creation_client_tunnel.sh $STARTPOINT_IP $ENDPOINT_IP $RELAY_IP $ENTRY_PORT
docker exec -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_relay_stepstone_1") /scripts/ssh-tunnel-creation_tunnel_server.sh $STARTPOINT_IP $ENDPOINT_IP $RELAY_IP $OUTWARD_PORT $SSH_SERVER_IP
###############################################################################################
sleep $DURATION
for ((i=1; i<=REPEAT; i++))
do
    START=$(date +%s)
    echo "Repeat Nr " $i
    rm -f $PWD/scripts/localhost-*

    array=()
    while read line ; do
        array+=($line)
    done < <(python3 ../trafficgeneration.py -s ${IP_RANGE})
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "1. took $DIFF seconds"
    NETCAT_PARA1=${array[0]}
    NETCAT_PARA2=${array[1]}
    NETCAT_PARA3=${array[2]}

    NETCAT_PARA4=${array[3]}
    NETCAT_PARA5=${array[4]}
    NETCAT_PARA6=${array[5]}

    DELAY_PARA1=${array[6]}
    DELAY_PARA2=${array[7]}
    DELAY_PARA3=${array[8]}
    DELAY_PARA4=${array[9]}
    DELAY_PARA5=${array[10]}
    DELAY_PARA6=${array[11]}
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "2. took $DIFF seconds"
    rm -f scrapy/spider_${PROJECT_NAME}.py
    cp scrapy/spider_backup/spider.py scrapy/spider_${PROJECT_NAME}.py
    sudo chmod 777 scrapy/spider_${PROJECT_NAME}.py
    sed -i "s/PLACEHOLDERURL/${IP_RANGE}/g" scrapy/spider_${PROJECT_NAME}.py

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
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "3. took $DIFF seconds"
    ###########################################################################################
    $PWD/scripts/container_tc.sh ${PROJECT_NAME}_relay_startpoint_1 $DELAY_PARA1 $DELAY_PARA2
    $PWD/scripts/container_tc.sh ${PROJECT_NAME}_relay_endpoint_1 $DELAY_PARA5 $DELAY_PARA6
    $PWD/scripts/container_tc.sh ${PROJECT_NAME}_relay_stepstone_1 $DELAY_PARA3 $DELAY_PARA4
    #############################################################################################
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "4. took $DIFF seconds"
    #rm -f $PWD/scripts/localhost-*
    #rm -f $PWD/scripts/localhost-17-${IP_RANGE}-reverse.txt
    #rm -f $PWD/scripts/localhost-19-${IP_RANGE}-reverse.txt
    #rm -f $PWD/scripts/localhost-18-${IP_RANGE}.txt
    #rm -f $PWD/scripts/localhost-16-${IP_RANGE}.txt

    #echo "Start chaff in $DURATION seconds...."
    #sleep $DURATION
    # Start first chaffer from the the beginning of the first tunnel, aka 172.${IP_RANGE}.238.7, 
    #to the end of the first tunnel, aka 172.${IP_RANGE}.238.9
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_send") /usr/share/scripts/netcat_send.sh $DURATION localhost 18 6000 $NETCAT_PARA1 $NETCAT_PARA2 $NETCAT_PARA3
    # Start third chaffer from the the beginning of the second tunnel, aka 172.${IP_RANGE}.238.8, 
    #to the end of the second tunnel, aka 172.${IP_RANGE}.238.9
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_stepstone") /usr/share/scripts/netcat_send.sh $DURATION localhost ${IP_RANGE} 6002 $NETCAT_PARA4 $NETCAT_PARA5 $NETCAT_PARA6
    # Start the reverse chaffer from the the end of the first tunnel, aka 172.${IP_RANGE}.238.9, 
    # to the beginning of the first tunnel, aka 172.${IP_RANGE}.238.7
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_stepstone") /usr/share/scripts/netcat_send_reverse_server.sh $DURATION localhost 19 $NETCAT_PARA1 $NETCAT_PARA2 $NETCAT_PARA3
    #sleep 0.05
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_send") /usr/share/scripts/netcat_receive_reverse_client.sh localhost 19 6001 $IP_RANGE
    # Start the reverse chaffer from the the end of the first tunnel, aka 172.${IP_RANGE}.238.9, 
    # to the beginning of the first tunnel, aka 172.${IP_RANGE}.238.8
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_receive") /usr/share/scripts/netcat_send_reverse_server.sh $DURATION localhost 17 $NETCAT_PARA4 $NETCAT_PARA5 $NETCAT_PARA6
    #sleep 0.05
    #docker exec -d -it $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_stepstone") /usr/share/scripts/netcat_receive_reverse_client.sh localhost 17 6003 $IP_RANGE
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "5. took $DIFF seconds"
    ###############################################################################################
    echo "Sending through tunnel in $DURATION seconds...."
    timeout -k $(($DURATION2+10)) $DURATION2 docker exec -ti $(sudo docker ps -aqf "name=${PROJECT_NAME}_spider_1") scrapy runspider "scrapy/spider_${PROJECT_NAME}.py"; EXIT_CODE=$?
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "6. took $DIFF seconds"
    echo $EXIT_CODE
    
    if [ $EXIT_CODE -ne 124 ] && [ $EXIT_CODE -ne 137 ]; then
    	rm data/${PROJECT_NAME}_relay_stepstone-${CAPTURETIME}-sc${SCENARIO}-$REPNUM.pcap
    else
    	python3 ../pcap_to_deepcorr.py -p "data/${PROJECT_NAME}_relay_stepstone-${CAPTURETIME}-sc${SCENARIO}-$REPNUM.pcap" -n "data/${PROJECT_NAME}"
        echo ${PROJECT_NAME}_relay_stepstone-${CAPTURETIME}-sc${SCENARIO}-$REPNUM "," $NETCAT_PARA1 "," $NETCAT_PARA2 "," $NETCAT_PARA3 "," $NETCAT_PARA4 "," $NETCAT_PARA5 "," $NETCAT_PARA6 "," $DELAY_PARA1 "," $DELAY_PARA2 "," $DELAY_PARA3 "," $DELAY_PARA4 "," $DELAY_PARA5 "," $DELAY_PARA6 >> data/${PROJECT_NAME}_PARAMS.txt
        rm data/${PROJECT_NAME}_relay_stepstone-${CAPTURETIME}-sc${SCENARIO}-$REPNUM.pcap
    fi
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "7. took $DIFF seconds"    
    #sudo docker restart $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_send")
    #sudo docker restart $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_stepstone")
    #sudo docker restart $(sudo docker ps -aqf "name=${PROJECT_NAME}_netcat_receive")
    sudo docker restart $(sudo docker ps -aqf "name=${PROJECT_NAME}_tcpdump_relay_stepstone")
    sudo docker restart $(sudo docker ps -aqf "name=${PROJECT_NAME}_spider_1")
    END=$(date +%s)
    DIFF=$(( $END - $START ))
    echo "8. took $DIFF seconds"
done

sleep 1
teardown