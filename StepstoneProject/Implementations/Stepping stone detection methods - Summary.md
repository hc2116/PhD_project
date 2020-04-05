## Stepping stone detection methods - Summary



#### Correlation

Correlating TCP/IP Packet contexts to detect stepping-stone intrusion





#### Counting

###### Monitoring Network Traffic to Detect Stepping-Stone Intrusion

J Yang, B. Lee, 2008, Houston, 8

- time interval of length t
- packets captured N_1 and N_2 in both connections during interval
- N_1-N_2 follows random walk process, must be close to yero

###### Detection of Interactive Stepping-Stones: Algorithms and Confidence Bounds

Blum, 2004, Carnegie Mellon, 253

- difference between send packets in two connections
- difference is bounded iff the connections are relayed
- needs large number of packets if small amount of chaff is present
- mathematical paper

###### Detecting encrypted stepping-stone connections

T. He, L. Tong, 2007, Cornell, 93

DBDC: detect-bounded-memory-chaff

- chaff packet injection rate can be at least 1/(1+gamma*delta) of original traffic, gamma= parameter of Poisson distribution, delta is upper bound of packet delays
- also "Detecting  encrypted  interactive  stepping-stone connections", 2006, 14 for bounded memory (very similar)

###### Stepping-Stone Detection Via Request-Response Traffic Analysis

Stephen Huang, J Yang, 2007, Houston, 10

- analyze  correlations between the frequencies  of  the  cumulative  numbers  of  packets  sent  in  incoming  and outgoing   connections
- supplementing of Blum et al.
- paper incomplete as experiments did not yield all the required results



#### RTT



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



###### RTT-based Random Walk Approach to Detect Stepping-Stone Intrusion 

J Yang, Zhang, 2015, Columbus State, 5

- Same approach as above to mine RTTs
- Compute number N of RTTs for incoming and for outgoing connection, compute N_in-N_out
- If relayed, value should be more or less zero
- If the value changes, but is bounded by Gamma, this indicates a stepping stone
  - value modelled as random walk

###### Detecting Stepping-Stone Intruders with Long Connection Chains

W. Ding, M. Hausknecht, Stephen Huang, 2009, Houston, 12

- Estimated round trip time in long connection chains
- applied to keystroke sessions, Time Diff=RTT + user delay time



###### Detecting Stepping-Stone Intruders by Identifying Crossover Packets in SSH Connections

Stephen Huang, H. Zhang, 2016, Houston, 5

Improves above

- distinguish and identify long chains from short ones
- if connection chain is long, RTT may be longer than time between two keystrokes

###### Detection of stepping stone attack under delay and chaff perturbations

L. Zhang, 2006, Iowa state, 53

The   authors   assumed   time synchronization   between   hosts,   bounded   delay,   chaff   perturbation independent of the original flow, and no packet loss

should include this

However, stepping-stone traffic  can  be detected if chaff is only inserted in the departing stream

###### Performance of neural networks in stepping-stone intrusion detection

H. Wu, Stephen Huang, 2008, Houston, 11

- Uses packet variables to compute RTT
- Only short interval required
- Performance varies
- extended in "Neural  networks-based  detection  of stepping-stone  intrusion" (29 citations, 2010)



######  Efficient multi-dimensional flow correlation

W. Strayer, 2007, BBN Technologies, 12

Ten characteristics, PCA to select proper characteristics which contribute most variance for all flows and least variance for correlated flows, 

advantages: track more than one flow, not scaling with N^2



###### Efficient Detection of Delay-Constrained Relay Nodes

Coskun, Memon, 2007, Polytechnic University NY, 9 

- check IP addresses from and to a node (potential stepping stone) in sequential windows
  - if two pairs occur together often, likely a stepping stone pair
  - traffic needs to be sparse, with many empty windows, as well as a delay constraint



###### Detecting Connection-Chains: A Data Mining Approach

A. Almulhem, I. Traore, 2008, U. of Victoria, Canada, 9

- association rule mining between inbound and outbound packets
- claim to achieve TPR of 100% and FPR of 0%
- not affected by chaff and delay



###### Improving   Stepping-Stone   Detection   Algorithms   using   Anomaly Detection   Techniques

Kampasi, Y. Zhang, 2007, Houston, 11

Anomaly engine for:

- response-time method that detects jitter anomalies, 
- edit-distance method to detect chaff 
- causality method to detect chaff



###### Detecting Anomalies in Active Insider Stepping Stone Attacks

A, Kampasi, Crescenzo, Abhrajit Ghosh, 2011, Houston&Princeton, 13

three anomaly detection algo to detect presence of jitter and chaff

- response-time based
  - group packets in ON OFF periods
  - detect delays
  - if ack-packet takes longer than RTT+d_t
    - anomalous if threshold and packet ratio is exceeded
- edit-distance based
  - detect chaff
  - break into ON periods
  - for each period, compare the interarrival times in forward with backwards direction
  - should be similar, calculate edit distance
- causality-based
  - check if there are no or more than one on periods in one direction during an on period in the other



###### Detecting Chaff Perturbation on Stepping-Stone Connection

Stephen Huang, Y. Kuo, 2011, Houston, 6

Anomaly-based, complements correlation-based techniques

Our study  shows  the  probability  distribution  of  the  inter-arrival  time  of  a  chaffed  connection  differs  from  that  of  one  without  chaff.


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



