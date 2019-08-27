#!/bin/bash                                                                                                                                                                                                                                                                       

CONTAINER=$1
PORT=$2
PORTNUM=$3
                                                                                                                                                                                                                   function get_container_veth() {
  # Get the process ID for the container named ${CONTAINER}:
  pid=$(docker inspect -f '{{.State.Pid}}' "${CONTAINER}")
  #pid=$CONTAINER

  # Make the container's network namespace available to the ip-netns command:
  mkdir -p /var/run/netns
  ln -sf /proc/$pid/ns/net "/var/run/netns/${CONTAINER}"

  # Get the interface index of the container's eth0:
  index=$(ip netns exec "${CONTAINER}" ip link show eth0 | head -n1 | sed s/:.*//)
  # Increment the index to determine the veth index, which we assume is
  # always one greater than the container's index:
  let index=index+1

  # Write the name of the veth interface to stdout:
  ip link show | grep "^${index}:" | sed "s/${index}: \(.*\):.*/\1/"

  # Clean up the netns symlink, since we don't need it anymore
  rm -f "/var/run/netns/${CONTAINER}"
}

veth_full=$(get_container_veth $CONTAINER)

veth=${veth_full%@*}                                                                                                                                                                                 

tc qdisc replace dev $veth root handle 1: htb
tc class add dev $veth parent 1: classid 1:1 htb rate 1000mbit
tc filter add dev $veth parent 1: protocol ip prio 1 u32 flowid 1:1 match ip $PORT $PORTNUM 0xffff
tc qdisc add dev $veth parent 1:1 handle 10: netem loss 100%
     
#tc qdisc replace dev $veth root netem loss 100% 

