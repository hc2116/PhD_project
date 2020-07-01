## Outline of planned DetGen extension



#### What we can currently do

We have 26 scenarios for different protocols and malicious activity. From these, we can generate "atomic" traffic traces (and now also system logs).

Characteristics:

- Ground truth due to "atomic" nature of traces
- Modularity since senarios are independent
- Scalability due to stand-alone nature of container scenarios
- Variability due to randomisation, network emulation, subscenarios

What we are not doing so far is embed these traces in a larger network context.


#### Motivation

- Several testbeds (give examples) exist to allow the simulation of network-like settings in a scalable manner. However, these settings are always static, i.e. any generated data comes from the same network topology with the same services etc.

  Furthermore, there are no attempts at fusing network traffic and other types of data into one dataset

- Larger network traffic datasets do no contain any ground truth labels about the stuff going on (apart from malicious/benign labels)

- Attack simulation tools and testbeds exist, but to my knowledge only for specific individual attacks, not for multi-stage attack. 

- Due to the self-sufficiency of the docker containers, our existing framework provides an easy way to create communicating networks in a randomised manner. 
  

#### Goals

- Embed all scenarios in a Mininet framework in order to allow the fast inclusion of switches, routers, etc. (called Containernet)
- Design a launch script that 
  - creates a network topology that is randomised to some degree
  - populates the topology with docker containers and corresponding IP addresses
  - launches scenarios for the containers in randomised intervals according to a suitable distribution
- Include  the  collection  of  application  logs  and  system  call  logs  for  each  container. 
  - add a tag mechanism to match logs with the corresponding traffic captures and the same ground truth labels.



We have already figured out how to embed the scenarios in Mininet and how to collect the system logs. The other goals here so far should be relatively easy to fulfil.



- Another goal inspired by Gudmund is to add mechanism (he called it domain specific language) to combine the implemented attack scenarios into multi-step attacks. The specific combination of attacks should be variable to add variability and different angles/dimensions to the data of the multi-stage attack.
  - Creating one or more attack profiles (such as the kill-chain, but more refined) that follow define the purpose of the attack and what actions (reconnaissance, pivoting, backdoors, etc.) are involved .
  - For each action, collect a number of potential attacks that are suitable tools to achieve the action (such as SQL injections to steal user credentials, brute-forcing to gain access on a machine)
  - Create an attack launch script for each attack profile that
    - defines how many actions of each type are needed for the given topology to get to the destination
    - for each action, selects an appropriate implemented attack (in a randomised manner)
    - selects the hosts that are targeted in the attack (in a randomised manner)
      Furthermore, for each action there might be unsuccessful attemps at a number of hosts before success, which should be included
    - Conducts each action in the sequence with some time interval separating the actions



#### Related work


######ContainerNet or MeDICINE: Rapid prototyping of production-ready network services in multi-PoP environments


###### Reproducible Network ExperimentsUsing Container-Based Emulation
<img src="Rep_cont.png" width="50%">.

Aims at providing performance isolation for benchmarking

Goals: 

**Functional realism.**
The system must have the same func-tionality as real hardware in a real deployment, and shouldexecute exactly the same code.

**Timing realism**
The timing behavior of the system must be close  to  (or  indistinguishable  from)  the  behavior  of  de-ployed hardware. The system should detect when timing re-alism is violated.

**Traffic realism.**
The system should be capable of generat-ing and receiving real, interactive network traffic to and fromthe Internet, or from users or systems on a local network.In addition to providing realism, the system must make iteasy to reproduce results, enabling an entire network experi-ment workflow – from input data to final results – to be easilycreated, duplicated, and run by other researchers:

**Topology flexibility.**
It should be easy to create an experi-ment with any topology.

**Easy replication.**
It should be easy to duplicate an experi-mental setup and run an experiment.Low cost.It should be inexpensive to duplicate an experi-ment, e.g. for students in a course.




#### Contribution

- A specialised reproducible testbed that provides data for ML-based intrusion detection. Similar to the original DetGen paper, we should focus on benefits for ML since current solutions are lacking here. In a nutshell, the idea is that this framework can be used to create multiple datasets of networks with slightly different properties, which would make the training and evaluation of ML-based methods much more in-depth. In particular, the following features distinguish it from other testbeds:
	- automatised and randomised topology-creation. The randomisation aspect particularly important for network-wide methods (graph-based for example) that are influenced by the topology, where a regular dataset such as LANL 15 or CICIDS 17 only provide one topology example each, which is insufficient for a proper evaluation. 
	- generation of randomised execution script that steers when, where and which data exchanges are conducted through our container scenarios. By being able to generate such an execution script, we can tune the amount of traffic for different traffic types/scenarios in a given dataset and make events that are rare in one dataset appear more common in another dataset. We can also add niche-services in one dataset that are not included in another dataset (works better if we have more scenarios). Again, this is not even remotely addressed by existing datasets. 
	- Multi-stage attack simulation: Attack simulation tools and testbeds exist, but to my knowledge only for specific individual attacks, not for multi-stage attack. Due to the randomised topology, we could potentially provide a very diverse selection of multi-stage attacks that are unique for each topology. 
	- We will include the possibility to pass certain requirements to generation of the topology and execution script (such as a minimum of subnets, or which services should/should not be included). This will allow researchers to create data taylored to their methods, and generate sufficient amounts to effectively train ML-methods.
	- We could construct a API that allows the live-testing of an IDS (probably just for python) to let researchers evaluate how operational their methods are.  
	- All the distinguishing features of the existing DetGen-framework, but scaled to produce traffic for a whole network

- We can also provide an examplary dataset that includes data from multiple networks as well as some attack data. This can be used for some experiments such as the ones we performed for the previous DetGen paper, and highlight the benefits of our approach. A more comprehensible dataset should include the multi-stage attack scenarios though as this would be a very strong feature for a dataset. 
