#!/bin/bash                                                                                                                                                                                                                                                                       

CONTAINER=$1
MEAN=$2
SD=$3
MS="ms"
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
                                                                                                                                                                                                                                                                                  
# Example just with 40% loss                                                                                                                                                                                                                                                      
#tc qdisc replace dev $veth root netem loss 1%                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                  
# Example delay                                                                                                                                                                                                                                                                    
sudo tc qdisc replace dev $veth root netem delay $MEAN$MS $SD$MS distribution normal                                                                                                                                                                                                        
#sudo tc qdisc replace dev $veth root netem loss random 10% 10% ecn

#sudo tc qdisc add dev $veth root red min 5 max 20 limit 25 avpkt 10 probability 0.8 ecn
                                                                                                                                                                                                                                                                                
