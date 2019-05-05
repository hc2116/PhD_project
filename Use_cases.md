### Project thoughts:


- Project start: September, possibly for three months, depending how much time is needed to achieve goals
- Project will be about generation of realistic traffic with attacks
	- We both need data that contains benign traffic as well as attack traffic that we want to examine
	- I could apply packet-sequence modelling developped during the summer
	- Docker framework could be used as starting point, although we want to

- Interesing use-cases they presented:
	- Stepping-stone detection
	- Unusual User Agents
	- Maybe session-hijacking, etc. (man-in-the-middle attacks)
- These all need appropriate datasets that contain enough benign traffic to train a model

- BT might have people with knowledge about attack traffic, networking, etc. and resources to help?
- It is easier to benefit from people at BT than developing technical model where the detailed knowledge might not be there

- If that is objected, I would suggest working on traffic disaggregation


&nbsp; 
&nbsp;
&nbsp;
&nbsp;


- Additional things: 
	- Do I have to get involved with Robs project? Should be starting soon right?
	- NVIDIA statement (how much time to put into it? How likely we get it? Wait till paper is submitted?)

&nbsp; 
&nbsp;
&nbsp;
&nbsp;
&nbsp; 
&nbsp;
&nbsp;
&nbsp;
&nbsp; 
&nbsp;
&nbsp;
&nbsp;



###David's comments:
- Drill down on the difference between acamedic environment and real-world
- Good position on publications as we have industrial validation for the relevance for industry
- Suggest discussion on the industry situation on the data that they are collecting,
- think about the future/change in network infrastructure
	- is the home-application interesting
	- devices going to the edge (5G computing pushed to periphery)
- Present results from paper
- Fadi El-Mousse at BT
- Shadowserver people
- Dell Secureworks
- Agenda-item: Find out what they are working on
- Pitch idea of conversation fingerprinting
- Maybe have a little presentation in front of interested people


### Alex Use-Cases






Hi All, 
 
Good to meet up the other week. David, you asked about a project that Henry could get his teeth into for a few months. I thought that in advance of our catch up call this afternoon I’d send across some of the most pertinent security threat detection use cases that we are always interested in finding new techniques for. Failing being able to anonymise and distribute some BT production data for you to work with (it is looking like it will take significant time to get this far), my suggestion would be to look at which one (or many) of these use cases looks easiest to develop against using public domain or otherwise synthetic datasets. Your thoughts on any of these most welcome. We may have to do a bit of digging ourselves before answering in-depth questions though. 
 
Regards,
Alex 
 
 
#### Stepping-stone detection
Aim to implement an algorithm to detect use of potentially malicious stepping stones within the corporate network with a manageable proportion of false positives.
Some example papers on the concept are: 
http://cs.unc.edu/~fabian/course_papers/Stepping-Stones.pdf
https://rd.springer.com/content/pdf/10.1007%2F978-3-540-30143-1_14.pdf
Use of multiple taps within an enterprise network. 
Several feed types/protocols may be used, e.g. NetFlow, SSH, RDP.
 

#### C2 & Malware Beaconing Detection
Detect unusual changes in network behaviour (e.g. DNS lookups) which might enable detection of C2 infrastructure.
Data exfiltration in DNS may be another indicator, e.g. high numbers of unique non-textual hostname part in requests (there may or may not be a response - currently we only have response logs; we have a backlog item to add DNS request logs).
Regular DNS requests (or responses) between a host and a domain may carry C2 traffic. The regularity may be approximate because of jitter deliberately added by the malware, as well as because of hosts being shut-down or disconnected. There may be some non-regular traffic in between, e.g. to respond to an initial command. The periodic unit may be a set of requests, i.e. a group of requests that are not periodic in themselves may be repeated regularly as a group. Domain names themselves might be cycled, i.e. successive requests at regular intervals made to each domain name in a series of domain names.
 

#### Behavioural change detection
Detect significant, but not previously characterised, changes in the pattern of activity of devices in an enterprise network that indicate potentially malicious activity with high confidence. Detection of deviation from an established, consistent pattern of behaviour for a host (or user or application). May not be effective on devices with highly variable normal behaviour. May not be sufficiently indicative on its own, but may contribute to scoring other alerts for the host. Could apply to almost any protocol.

 
#### Port Scanning
Detection of port scanning. May be single host multiple ports, or single port multiple hosts, or a combination. 
May be increased attention to a new port for scanning. May be at a low rate to avoid normal detection.
Location of probes on the exit from a datacentre may limit our ability to detect scanning.
Port scanning probably occurs quite extensively from normal network management. How can this be eliminated?
 
 
#### Unusual User Agents
Identify user agents that are untypical or new for a user and are not common across an enterprise network.
