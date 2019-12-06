#!/bin/sh
DURATION=$1
IP=$2
PORT1=$3
PORT2=$4

PARA1=$5
PARA2=$6
PARA3=$7

[ -z "$PARA1" ] && PARA1=0.1
[ -z "$PARA2" ] && PARA2=10000
[ -z "$PARA3" ] && PARA3=10


sleep 1
echo "hello Henry"
i=1
while true
do

    Pi=`echo "4*a(1)" | bc -l`
    
    RNP0=$((1 + RANDOM % 30000))
    RNP1=$((1 + RANDOM % 30000))
    RNP2=$(echo "sqrt(-2*l($RNP0/30001))*s($Pi*$RNP1/30001)" | bc -l)
    RNP3=$(echo "$PARA1*$RNP2+0.000001" | bc )
    sleep $RNP3
    ################

    RN=$((1 + RANDOM % 30000))
    RN2=$(echo "$PARA2*(s((0.5*$RN/32767)*$Pi)/c((0.5*$RN/32767)*$Pi))" | bc -l)
    RN3=$(echo "$PARA3+(2*$RN2)/2" | bc )
    RN33=$(dc -e "[$RN3]sM 1000000d $RN3<Mp")
    User=$(cat /dev/urandom | tr -dc 'a-z' | fold -w $RN33 | head -n 1)
    echo $User

    if [ $i -lt 2 ]; then
        sleep $(($DURATION))
    fi
    i=$((i + 1))
done | nc -p $PORT2 $IP $PORT1

sleep 2

