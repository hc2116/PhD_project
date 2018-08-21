

# Project

- Report tomorrow:
	- Connections/flows are itself closed entities in network traffic that give traffic a sort of granularity, i.e. they act as molecules/atoms of which traffic consists
	- different applications transmit data with a finite set of different connection protocols/implementations
	- Assumption: These different implementations leave different observable patterns in the connection that differentiate them from other implementations, but are consistent in one implementation
	- Aim: Discover different patterns in the observed connections in unsupervised manner to feed a model that classifies connections as members of different pattern groups
		- Having a model that can describes protocols/implementations that generate traffic in a relatively closed computer network gives us important benefits:
			1. We can identify the occurrence of implementations previously unobserved present in the traffic which might correspond a new program generating traffic, i.e. a possible intrusion
			2. We can with relatively low effort build a model that describes the frequency of occurrence of different implementation on different hosts and possibly correlate the temporal occurrency of different implementations to each other, thus building a behavioural model of  
			3. We investigate which protocols necessarily follow each other
		
	- These pattern groups should correspond to different application protocols/implementations for the model to have a real-world meaning 
		- That the model really groups connections according to implementations needs to be validated, i.e. we need to investigate 
			1. How well the model is able to differentiate between actual implementations/protols
			2. How consistently the model puts connections from the same implementation/protocol into the same group
	- Purpose of Nikola's project: Generate isolated connection data from different protocols/implementations that we can savely match to these
	
	
###Technical aspects/thoughts:	
- How do these patterns manifest themselves
	- Literature
	- My thoughts (in how many groups of packets data is transmitted, how full these packets are, ways how packets are acknowledged, how the connection reacts to lost packets)
	- insert image from clustering paper here showing bulks

- Current features of flows generator
- Purpose of autoencoder for clustering

#### Nicola's project

- Purpose of project
- What can be achieved?
- What I can do immediately
	- Test internal validity of project, the exact same action does not depend on the machine it is executed on
	- Test how consistent patterns are for similar actions using the same implementation
- We should generate multiple capture files for randomized data transmitted (right now strings with randomized length)
- Gather the features from the collected connections



- write down current thoughts on approach to overall project
  - autoencoder purpose
  - event correlation
  - datasets 
  - what are actions (on application level)
  - what can be identified as actions
  - think about research proposal?
  
- write down steps for experiment
  - which containers generate which traffic
  - internal validity
  - traffic similarities
  - traffic statistics that are automatically generated
  - traffic filter for unwanted packages
  - compare traffic with http protocol description etc.
  - investigate http testing tools (tools that test if traffic from website is fulfilling http requirements)
  
- investigate current traffic generation (especially the cic data!!!)
  - investigat

- Validate that ping and other scenarios are similar at different workloads, different environments (machines) etc.

- Compile list of datasets
  - investigate datasets in introduction of CIC paper
	- Look for survey on datasets
	- look for survey for artifical data generation
	- look for survey on behavioural characterisations
	- look at shadowserver

- Write down a list of approaches to cluster flows, finger printing, behavioural flow characterisation
	- comments, what has not been told
	- Think about second order features compared to first order features: What characterises a flow
	- Compile a little report with the questions

- Blind signal separation (wikipedia) (Cocktail party problem)
	- Another look at traffic desagragation, also look at the use of factorial HMMs (like Guilio said), Imperial Guys (Oliver P..., ... Helly)

- Investigate blackboard transmission for next call

# Done
- Look at BT Invitation (done)