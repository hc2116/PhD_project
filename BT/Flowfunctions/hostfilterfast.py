#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
#from Desktop.Project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
#from Desktop.Project.BT.Flowfunctions.hostfilterfunctions import *



########################################################################################################################
# CICIDS
########################################################################################################################




outputfilename="Desktop/Project/Data/CIC/Friday-WorkingHours_activity.csv"
outputfilename="Desktop/Project/Data/CIC/Friday-WorkingHours_activity_sampled.csv"

outputfilename="Desktop/Project/Data/CIC/Monday-WorkingHours_activity.csv"
outputfilename="Desktop/Project/Data/CIC/Monday-WorkingHours_activity_sampled.csv"


outputfilename="Desktop/Project/Data/CIC/Thursday-WorkingHours_activity.csv"
outputfilename="Desktop/Project/Data/CIC/Thursday-WorkingHours_activity_sampled.csv"

outputfilename="Desktop/Project/Data/CIC/Tuesday-WorkingHours_activity.csv"
outputfilename="Desktop/Project/Data/CIC/Tuesday-WorkingHours_activity_sampled.csv"

outputfilename="Desktop/Project/Data/CIC/Wednesday-WorkingHours_activity.csv"
outputfilename="Desktop/Project/Data/CIC/Wednesday-WorkingHours_activity_sampled.csv"



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)
Title="ABC"

values=[0,6,12,18,24,30]
values.extend([36])
Host1=Flows.iloc[:,values]

Hosts=["192.168.10.3","192.168.10.50","192.168.10.51","192.168.10.19","192.168.10.9","192.168.10.25"]

values=[0,6,12,18,24,30]
values=[x+1 for x in values]
values.extend([36])
Host1=Flows.iloc[:,values]


plt.plot(Host1.iloc[:,6],Host1.iloc[:,0], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,1], label="Out-stream")
plt.title("#Packets"+Title)
plt.xlabel("Minutes")
ax = plt.axes()
ax.xaxis.set_major_locator(plt.MaxNLocator(1))
#plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
plt.legend()
plt.show()
plt.plot(Host1.iloc[:,6],Host1.iloc[:,2], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,3], label="Out-stream")
plt.title("#bytes"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Host1.iloc[:,6],Host1.iloc[:,4], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,5], label="Out-stream")
plt.title("#IPs"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()


plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,0], label="In-stream")
plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,1], label="Out-stream")
plt.title("#Packets"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,2], label="In-stream")
plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,3], label="Out-stream")
plt.title("#bytes"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,4], label="In-stream")
plt.plot(Host1.iloc[0:100,6],Host1.iloc[0:100,5], label="Out-stream")
plt.title("#IPs"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()







outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33.txt"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)
Title="ABC"

outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33_sample.txt"




values=[0,1,2,3,4,5]
values.extend([6])
Host1=Flows.iloc[:,values]




plt.plot(Host1.iloc[:,6],Host1.iloc[:,0], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,1], label="Out-stream")
plt.title("#Packets"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Host1.iloc[:,6],Host1.iloc[:,2], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,3], label="Out-stream")
plt.title("#bytes"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Host1.iloc[:,6],Host1.iloc[:,4], label="In-stream")
plt.plot(Host1.iloc[:,6],Host1.iloc[:,5], label="Out-stream")
plt.title("#IPs"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()





















########################################################################################################################
# Data_May
########################################################################################################################
filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.txt"

from scapy.all import *
import re
#from Desktop.Project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.Project.BT.Flowfunctions.flowfunctions import *
from datetime import datetime


Flowcomp(filename,
          outputfilename,
          pcap=True,
          sampling=True)

import pandas as pd
import numpy as np
#import networkx as nx
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)
Title="33 80cl/15s sampled"

Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()

Flows.loc[Flows.SIP!="10.239.51.1","DIP"].value_counts()

Flows_network=Flows.loc[:,["Prot","SIP","DIP"]]

Flows_network["Bytes"]=Flows.SBytes+Flows.DBytes
Flows_network["LogBytes"]=np.log(Flows.SBytes+Flows.DBytes)
Flows_network["SIP_DIP"]=Flows_network.SIP+"_"+Flows_network.DIP

#Flows_network.SIP_DIP.value_counts().hist()


###############
max(Flows.Start)-min(Flows.Start)
datetime.fromtimestamp(max(Flows.Start)).strftime("%A, %B %d, %Y %I:%M:%S")
datetime.fromtimestamp(min(Flows.Start)).strftime("%A, %B %d, %Y %I:%M:%S")

start=int(np.floor(min(Flows.Start)))
stop=int(np.ceil(max(Flows.Start)))

Time=[]
Firstconns=[]
Secconns=[]
FirstIPs=[]
SecIPs=[]
FirstBytes=[]
SecBytes=[]
FirstBytesm=[]
SecBytesm=[]
FirstDursm=[]
SecDursm=[]
FirstDurs=[]
SecDurs=[]
t_diff=3
t_d=t_diff*60
for t in range(start,stop,t_d):
    Time.append((t-start)/60)
    Flows_t=Flows.loc[(Flows.Start>=t)&(Flows.Start<=(t+t_d))]
    Firstcon=Flows_t.loc[Flows_t.DIP=="10.239.51.1","SIP"].shape[0]
    Seccon=Flows_t.loc[Flows_t.SIP=="10.239.51.1","DIP"].shape[0]
    Firstconns.append(Firstcon)
    Secconns.append(Seccon)
    FirstIP=len(Flows_t.loc[Flows_t.DIP=="10.239.51.1","SIP"].unique())
    SecIP=len(Flows_t.loc[Flows_t.SIP=="10.239.51.1","DIP"].unique())
    FirstIPs.append(FirstIP)
    SecIPs.append(SecIP)
    FirstByte=sum(Flows_t.loc[Flows_t.DIP=="10.239.51.1","SBytes"]+Flows_t.loc[Flows_t.DIP=="10.239.51.1","DBytes"])
    SecByte=sum(Flows_t.loc[Flows_t.SIP=="10.239.51.1","SBytes"]+Flows_t.loc[Flows_t.SIP=="10.239.51.1","DBytes"])
    FirstBytes.append(FirstByte)
    SecBytes.append(SecByte)
    FirstByte=np.mean(Flows_t.loc[Flows_t.DIP=="10.239.51.1","SBytes"]+Flows_t.loc[Flows_t.DIP=="10.239.51.1","DBytes"])
    SecByte=np.mean(Flows_t.loc[Flows_t.SIP=="10.239.51.1","SBytes"]+Flows_t.loc[Flows_t.SIP=="10.239.51.1","DBytes"])
    FirstBytesm.append(FirstByte)
    SecBytesm.append(SecByte)
    ####################
    #FirstDurm=np.mean(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    #SecDurm=np.mean(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    #FirstDursm.append(FirstDurm)
    #SecDursm.append(SecDurm)
    #FirstDur=np.sum(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    #SecDur=np.sum(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    #FirstDurs.append(FirstDur)
    #SecDurs.append(SecDur)

plt.plot(Time,Firstconns, label="In-stream")
plt.plot(Time,Secconns, label="Out-stream")
plt.title("#Connections"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstIPs, label="In-stream")
plt.plot(Time,SecIPs, label="Out-stream")
plt.title("#IPs"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytes, label="In-stream")
plt.plot(Time,SecBytes, label="Out-stream")
plt.title("#Bytes"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytesm, label="In-stream")
plt.plot(Time,SecBytesm, label="Out-stream")
plt.title("av. bytes per connection"+Title)
plt.xlabel("Minutes")
plt.legend()
plt.show()
#plt.plot(Time,FirstDursm, label="In-stream")
#plt.plot(Time,SecDursm, label="Out-stream")
#plt.title("av. conn. curation"+Title)
#plt.xlabel("Minutes")
#plt.legend()
#plt.show()



