Things to do:

*** Develop a prototype mininet consisting of, say, 3-4 scenarios running simulataneously and gather the data

*** Clean up some Docker scenarios

*** Ensure that Dockerfiles use a minimal number of base images e.g there's no reason that one container uses alpine:3.6 as a base image whilst another uses alpine:3.7

*** Randomise names of containers and ip addresses in a manner that ensures that there are no collisions




## Requirements for scenario launch script

- Independent of network topology
	- Since we do not want to manually adjust this script for different network configuration, we probably need to input the network configuration to the launch script
	- research how to describe network topology
	- think about who makes the requests
		- usually the client, while the server just responds
		- in what scenarios is this not the case?
			- syncthing
			- bittorrent
			- mailx?
- what else is required to be specified in network topology?

- randomisation of host IP requesting this service
	- in a regular network, a large number of hosts can and will require different services, therefore we need to be able to generate for example FTP requests from different IP addresses and subnetworks to one or more servers. We might want to add and remove ftp containers to different network stacks on the fly to keep the overhead small

- must be able to run and generate data continuously

- collect data in pcap form and with ground truth labels in flow format 

- in terms of randomisation, we might want to draw the numbers of requests and the request times from certain distributions (not that important at this time how they are looking). 
	- to account for personal behaviours, we might draw the distribution hyperparameters (like mean and standard deviation) for each host from another distribution and fix them over the course of the data generation, such that request times for each host are drawn from slightly different distributions.
- with requests, I mean any action that starts a communication between containers

#### Design idea

- creat network topology with a list of hosts in network, along with IP address, subnetwork etc.
	- asign each host one or more functionalities, such as FTP server, SSH server, ...
- for each scenario, have lists of servers and clients with IP address and any other information describing the network topology as input
	- server:[server1, 192.168....., subnet1, server2,192.167....,subnet2]
	- client:[client1, 192.168....., subnet1,client2,192.167....,subnet2]
- have request distributions set for each scenario, but draw hyperparameters for each host individually
- draw request times (in advance or continuously?) for each host that can make
- once a request is supposed to be executed, start the corresponding container on the network stack of the host executing the request, execute the scenario, after finished take container down again (to avoid overhead, we might want to do the same for servers??) 


-verify if network topology is static in regular networks

Talk to David:
- computational difference if different activities are executed on seperate containers rather than on one machine like in the real world
- ground truth loss if the attach multiple computers to the same network stack? Is there a need to do that?





#### Logging

- Seems to be very easy
  - docker logs <containerID> > file.txt when the scenario is finished
  - don't think we need host logs
- Questions:
  - how to label them appropriately and match them with the corresponding flows?
  - Can it be included easily in containernet?