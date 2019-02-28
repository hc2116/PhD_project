
### Current thoughts on modeling approach

A major concern of reviewers was that the dataset is 
	1. small,
	2. synthetic,
	3. highly unbalanced,

so in other words not representative for real-world traffic, and that the unbalanced nature of the dataset hides the shortcomings of the model. To bolster the results, I applied the same methods (with some parameters tweaked for the RNN) to the dataset from the Los Alamos National Laboratory network (LANL). This is a dataset containing netflows from their corporate, internal computer network, and thus contains real-world traffic. It also contains attacks carried out by a "red team" on several machines in the network. These attacks are not synthetic, but stem from actual attacks, although it is not clear if they are representative for attacks from rogue agents.

To apply the methods to this dataset, I selected a set of machines with attacked and unattacked ones for comparison. As the network addresses are not labelled as to what kind of device they represent, I had to look for machines that appear to have behaviour and traffic of a personal computer. I am not sure if the methods are appropriate to other devices with less diverse traffic? 

As the traffic is purely internal, the number of destination ports responsible for the majority of the traffic is a lot higher, i.e. port 80, 443, etc. do not account for as much traffic as in the CTU data. For a number of computers, only about five ports had traffic percentages of more than 1 percent, so it seems that random destination ports are more common than in the CTU data.


The LANL dataset has far less attack traffic compared to benign one (which is a lot more realistic), it does not seem appropriate to classify machines as malicious based on the average score of the sessions in the test set.  As far less sessions are malicious,  their score would be almost completely depleted by all the benign sessions. Instead, the LANL data contains relatively accurate timestamps of the attacks, it is thus a lot easier to compare the flagged sessions with the ground truth labels. 


*Uninfected computer from CTU data*

![Clean1_CTU](Clean1_CTU.png)


*Another uninfected computer from CTU data*

![Clean2_CTU](Clean2_CTU.png)

*Infected computer from CTU data*

![Inf1_CTU](Infected_CTU.png)

*Clean computer from LANL data*

![Clean1_LANL](Clean1.png)

*Clean computers from LANL data*

![Clean2_LANL](Clean2.png)

![Clean3_LANL](Clean3.png)

*Clean computers from LANL data, the red lines mark known timestamps of malicious activity*

![Inf_LANL](Infected1.png)

![Inf2_LANL](Infected2.png)

The uninfected computers both for the CTU and for the LANL data have similar score distributions, with a few relatively isolated points hitting the 1.0 score or close, while the majority is far below. For the infected machine of the CTU data, you can see a lot of sessions hitting the 1.0 mark (however this is unrealistic as malicious traffic is not as prominent in real-life data). If you look at the infected LANL machines, you can see a few isolated alerts hitting the 1.0 mark at other points in time, but a lot of sessions hitting 1.0 at the attack times (not visible because they are all close together, but there are a lot more points at the attack times than at other times, by a ratio of about 5:100). 

I think it would be more reasonable to classify a machine as infected if a number of high-score flows within an expiration time are observed on a machine, as this would be both applicable to the CTU data and the LANL data.


Right now I am looking another dataset that is a mixture between the LANL and the CTU dataset, the UGR 2016 data (University of Grenada), to see get another validation source. They also have attacks with time-stamps, with some computers being attacked in a lab-environment (and thus resembling more the CTU data), and some computers in the wild also being subject to detected and examined attacks.



### Questions I have:

I managed to train all three models (MC, automaton, and RNN) on the data. However, I did not find a file or code that computes scores on the test data for the MC and the automaton approach, so I did not get to compute test scores for them yet. Is code for the evaluation available?

Also, I did not see anywhere how the plots with the precision, recall, etc. where generated. Is this also available somewhere?


