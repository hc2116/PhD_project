>Alex:
Good to meet up the other week. David, you asked about a project that Henry could get his teeth into for a few months. I thought that in advance of our catch up call this afternoon I’d send across some of the most pertinent security threat detection use cases that we are always interested in finding new techniques for. Failing being able to anonymise and distribute some BT production data for you to work with (it is looking like it will take significant time to get this far), my suggestion would be to look at which one (or many) of these use cases looks easiest to develop against using public domain or otherwise synthetic datasets. Your thoughts on any of these most welcome. We may have to do a bit of digging ourselves before answering in-depth questions though.

> Regards, Alex
 
 
### Stepping-stone detection
>Aim to implement an algorithm to detect use of potentially malicious stepping stones within the corporate network with a manageable proportion of false positives.
Some example papers on the concept are:
http://cs.unc.edu/~fabian/course_papers/Stepping-Stones.pdf
https://rd.springer.com/content/pdf/10.1007%2F978-3-540-30143-1_14.pdf
Use of multiple taps within an enterprise network.
Several feed types/protocols may be used, e.g. NetFlow, SSH, RDP.

* Very well written papers, but they both look at packet level data (often only flow level data available) 
* Hard to get hands on actual data that contains stepping stones (maybe we could generate data ourselves synthetically?)
* Is notion of stepping-stones/lateral movement in APT/kill chain still up-to-date?
* My MSc thesis was looking at similar notions
 
### C2 & Malware Beaconing Detection
>Detect unusual changes in network behaviour (e.g. DNS lookups) which might enable detection of C2 infrastructure.
Data exfiltration in DNS may be another indicator, e.g. high numbers of unique non-textual hostname part in requests (there may or may not be a response - currently we only have response logs; we have a backlog item to add DNS request logs).
Regular DNS requests (or responses) between a host and a domain may carry C2 traffic. The regularity may be approximate because of jitter deliberately added by the malware, as well as because of hosts being shut-down or disconnected. There may be some non-regular traffic in between, e.g. to respond to an initial command. The periodic unit may be a set of requests, i.e. a group of requests that are not periodic in themselves may be repeated regularly as a group. Domain names themselves might be cycled, i.e. successive requests at regular intervals made to each domain name in a series of domain names.
 
* Typical for botnets, where a lot of research on botnet detection has been done already
* C2 often via port 80, difficult to find attack patterns among diverse http traffic


### Behavioural change detection
>Detect significant, but not previously characterised, changes in the pattern of activity of devices in an enterprise network that indicate potentially malicious activity with high confidence. Detection of deviation from an established, consistent pattern of behaviour for a host (or user or application). May not be effective on devices with highly variable normal behaviour. May not be sufficiently indicative on its own, but may contribute to scoring other alerts for the host. Could apply to almost any protocol.

* Sounds very much aligned to the scope of my PhD project
* A bit vague, scope for a project would have to narrow down on certain aspects of behaviour

 
### Port Scanning
>Detection of port scanning. May be single host multiple ports, or single port multiple hosts, or a combination.
May be increased attention to a new port for scanning. May be at a low rate to avoid normal detection.
Location of probes on the exit from a datacentre may limit our ability to detect scanning.
Port scanning probably occurs quite extensively from normal network management. How can this be eliminated?
 
* I think port scanning detection has been sufficiently addressed already by research?
* https://content.iospress.com/articles/journal-of-computer-security/jcs154
 
### Unusual User Agents
>Identify user agents that are untypical or new for a user and are not common across an enterprise network.
 
* Very interesting and in line with behaviour change
* Could draw from browser fingerprinting


