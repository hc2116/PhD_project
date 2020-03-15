## Stepping stone detection methods - Summary





#### Random Walk techniques



###### Mining TCP/IP packets to detect stepping-stone intrusion

J Yang, Huang, 2007, University of Huston, 27

There is a minimum RTT time between send packet and its response
There should be some clustering around this time
If there is a chain of multiple stepping stones, you should see clustering around multiples of RTT time
Approach:

- Calculate deltas between send upstream and downstream packets in one connection, eliminate all that don't make sense, take union of al times
- MMD clustering with v clusters
- In each cluster, delete elements that are closer in time than others
- compute the likelihood R of the cluster representing a level by computing number of elements vs range 
- pick the highest likelihood clusters (two standard deviations higher than mean of ratio R)



###### Monitoring Network Traffic to Detect Stepping-Stone Intrusion

J Yang, B. Lee, 2008, Houston, 8

- time interval of length t
- packets captured N_1 and N_2 in both connections during interval
- N_1-N_2 follows random walk process, must be close to yero





###### RTT-based Random Walk Approach to Detect Stepping-Stone Intrusion 

J Yang, Zhang, 2015, Columbus State, 5

- Same approach as above to mine RTTs
- Compute number N of RTTs for incoming and for outgoing connection, compute N_in-N_out
- If relayed, value should be more or less zero
- If the value changes, but is bounded by Gamma, this indicates a stepping stone
  - value modelled as random walk

###### Detection of Interactive Stepping-Stones: Algorithms and Confidence Bounds

Blum, 2004, Carnegie Mellon, 253

- difference between send packets in two connecctions
- difference is bounded iff the connections are relayed
- needs large number of packets if small amount of chaff is present
- mathematical paper

###### Detecting encrypted stepping-stone connections

T. He, L. Tong, 2007, Cornell, 93

DBDC: detect-bounded-memory-chaff

- chaff packet injection rate can be at least 1/(1+gamma*delta) of original traffic, gamma= parameter of Poisson distribution, delta is upper bound of packet delays

###### Detecting Stepping-Stone Intruders with Long Connection Chains

W. Ding, M. Hausknecht, Stephen Huang, 2009, Houston, 12

- Estimated round trip time in long connection chains
- applied to keystroke sessions, Time Diff=RTT + user delay time

###### Detecting Stepping-Stone Intrudersby Identifying Crossover Packets in SSH Connections

Stephen Huang, H. Zhang, 2016, Houston, 5

Improves above

- distinguish and identify long chains from short ones
- if connection chain is long, RTT may be longer than time between two keystrokes



#### Watermarking

###### Robust correlation of encrypted attack traffic through stepping stones by flow watermarking.

X. Wang, D. Reeves, 2011, North Carolina, 41

- makes no assumption about the distribution of interpacket timing intervals
- makes these assumptions about timing perturbation:
  - delay is bounded
  - all packets are kept
  - watermarking embedding and decoding are secrets
- read more how it is done2q

###### A novel network flow watermark embedding model for efficient detection of stepping-stone intrusion based on entropy 

Y Chen, S. Wang, 2016, Huaqiao Uni, 2

The authors proved analytically and verified by experiment that the proposed scheme is robust for timing perturbation by intruders and the embedded watermark is invisible for intruders





#### Chaffing

###### Sniffing and Chaffing Network Traffic in Stepping-Stone Intrusion Detection

J. Yang, Y. Zhang, Columbus state