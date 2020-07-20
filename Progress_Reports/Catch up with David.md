## Catch up with David



#### DIMVA-paper 

- anything to discuss?



#### Project Rob

- At the moment working on generating traffic dataset for larger networks
  - with modifiable topology
  - non-deterministic usage profiles
  - usage of containernet (version of mininet)
  - collect data in pcap form and with ground truth labels in flow format 
- Later: 
  - create datasets that represent how attacks operate under different topologies
  - merge with log files
  - ...
- Questions for David:
  - computational difference if different activities are executed on seperate containers rather than on one machine like in the real world
  - ground truth loss if the attach multiple computers to the same network stack? Is there a need to do that?

#### Video relay

- absolutely no papers on proxy detection from ISP perspective
- compact problem
- but:
  - no data available
  - no research on how these illegal proxy servers operate (are they compressing video, transforming in other protocols, ....) --> no sources for problem relevance and validity of our approach
  - dependent on BT for either data or expert guidance what the constraints of the problem are
- Started implementing streaming docker scenario, first relay via ssh tunnels --> other approaches?
- Michael said he has some developments to talk about at next call, I also asked for 



#### QUIC/HHTP3

- a number of anomaly-detection approaches for regular http
  - most on requests (CSIC 2010 dataset)
- nothing yet on QUIC/http3 or even specifically for http2
- Quoted from NGINX 2019 presentation:
  - since protocol new and things like stack optimization etc still to catch up
  - "since it's all user-space, there is a possibility to make changes to protocol very rapidly"
    - "higher attack surface than you would have over more layered approach with TCP and http on top"
- Currently often blocked by firewalls as they are not adapted to it and cannot perform security checks or deep packet inspection yet
- However, I think only useful if you pass encryption and look at the http-communication itself
  - either host based solution or encrypt-decrypt firewalls (also called SSL bump?)
- Otherwise a stream of packets that is significantly more random than regular TCP-http (due to multiplexing)
- Nothing on vulnerabilities or attacks yet
- Need to find a potential attack angle for which we develop modelling approach
  - For example, model the response behaviour of a server for incoming requests



#### Current stepping stone project

- Similar to anomaly detection, there seems to be a widespread perception that connection correlation too high false alerts and able to be evaded
  - newer research more on connection chains or prevention through SDN
- Difficult to pitch new solution to this problem
- I think I would just do an evaluation of current methods, how effective they are in the presence of noise and delays
  - A lot of papers are not detailed enough to implement methods ....