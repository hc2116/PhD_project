#!/bin/sh
DURATION=$1
PORT1=$2

i=1
while true
do
    Pi=`echo "4*a(1)" | bc -l`
        
    RNP0=$((1 + RANDOM % 30000))
    RNP1=$((1 + RANDOM % 30000))
    RNP2=$(echo "sqrt(-2*l($RNP0/30001))*s($Pi*$RNP1/30001)" | bc -l)
    RNP3=$(echo "0.1*$RNP2+0.01" | bc )
    sleep $RNP3
    ################

    RN=$((1 + RANDOM % 30000))
    RN2=$(echo "1000*(s((0.5*$RN/32767)*$Pi)/c((0.5*$RN/32767)*$Pi))" | bc -l)
    RN3=$(echo "5+(2*$RN2+1)/2" | bc )
    User=$(cat /dev/urandom | tr -dc 'a-z' | fold -w $RN3 | head -n 1)
    echo $User

    if [ $i -lt 2 ]; then
        sleep $(($DURATION))
    fi
    i=$((i + 1))
done | nc -l 172.16.238.18 $PORT1

sleep 2

