#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
#from Desktop.Project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.Project.BT.Flowfunctions.flowfunctions import *

###############################################################################################################################
filename="Desktop/Project/BT/Data_Adi/stepping-stone-randomIPs.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/stepping-stone-randomIPs_flow.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv("Desktop/Project/BT/Data_Adi/stepping-stone-randomIPs_flow.txt")


Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()


Flows.iloc[:,4:24].head()
Flows.iloc[:,24:44].head()

Flows.SYN2.sum()
Flows.shape


###############################################################################################################################
filename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new_flow.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
import numpy as np
import networkx as nx
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)


Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()



Flows_network=Flows.loc[:,["Prot","SIP","DIP"]]

Flows_network["Bytes"]=Flows.SBytes+Flows.DBytes
Flows_network["LogBytes"]=np.log(Flows.SBytes+Flows.DBytes)
Flows_network["SIP_DIP"]=Flows_network.SIP+"_"+Flows_network.DIP

Flows_network.loc[Flows_network.SIP_DIP=="10.239.51.1_12.0.0.2","Bytes"].hist()
Flows_network.loc[Flows_network.SIP_DIP=="10.239.51.1_12.0.0.2","LogBytes"].hist()

Flows_network.SIP_DIP.value_counts()



G=nx.from_pandas_edgelist(Flows_network.iloc[0:1000,:],
                          source="SIP",
                          target="DIP")

nx.draw(G)


###############################################################################################################################
filename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-100-server-new/stepping-stone-100clients-100server-new.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-100-server-new/stepping-stone-100clients-100server-new_flow.txt"
filename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new_flow.txt"


Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)

Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()

Flows.loc[Flows.SIP!="10.239.51.1","DIP"].value_counts()

Flows_network=Flows.loc[:,["Prot","SIP","DIP"]]

Flows_network["Bytes"]=Flows.SBytes+Flows.DBytes
Flows_network["LogBytes"]=np.log(Flows.SBytes+Flows.DBytes)
Flows_network["SIP_DIP"]=Flows_network.SIP+"_"+Flows_network.DIP

Flows_network.SIP_DIP.value_counts().hist()


###############
max(Flows.Start)-min(Flows.Start)

start=int(np.floor(min(Flows.Start)))
stop=int(np.ceil(max(Flows.Start)))

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
t_d=5
for t in range(start,stop,t_d):
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
    FirstDurm=np.mean(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    SecDurm=np.mean(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    FirstDursm.append(FirstDurm)
    SecDursm.append(SecDurm)
    FirstDur=np.sum(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    SecDur=np.sum(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    FirstDurs.append(FirstDur)
    SecDurs.append(SecDur)

Time=[5,10,15,20,25,30,35,40,45,50,55,60]
Time=list(range(5,161,5))
plt.plot(Time,Firstconns, label="In-stream")
plt.plot(Time,Secconns, label="Out-stream")
plt.title("#Connections, 100cl/1s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstIPs, label="In-stream")
plt.plot(Time,SecIPs, label="Out-stream")
plt.title("#IPs, 100cl/1s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytes, label="In-stream")
plt.plot(Time,SecBytes, label="Out-stream")
plt.title("#Bytes, 100cl/1s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytesm, label="In-stream")
plt.plot(Time,SecBytesm, label="Out-stream")
plt.title("average bytes per connection, 100cl/1s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstDursm, label="In-stream")
plt.plot(Time,SecDursm, label="Out-stream")
plt.title("average conn curation, 100cl/1s")
plt.xlabel("Minutes")
plt.legend()
plt.show()




########################################################################################################################
# Data_April
########################################################################################################################
filename="Desktop/Project/BT/Data_Adi/Data_April/Client-Server-merged-123.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_April/Client-Server-merged-123_flow.txt"
from scapy.all import *
import re
#from Desktop.Project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.Project.BT.Flowfunctions.flowfunctions import *


Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv(outputfilename)

Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()

Flows.loc[Flows.SIP!="10.239.51.1","DIP"].value_counts()

Flows_network=Flows.loc[:,["Prot","SIP","DIP"]]

Flows_network["Bytes"]=Flows.SBytes+Flows.DBytes
Flows_network["LogBytes"]=np.log(Flows.SBytes+Flows.DBytes)
Flows_network["SIP_DIP"]=Flows_network.SIP+"_"+Flows_network.DIP

Flows_network.SIP_DIP.value_counts().hist()


###############
max(Flows.Start)-min(Flows.Start)

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
t_d=5
for t in range(start,stop,t_d):
    Time.append(t-start)
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
    FirstDurm=np.mean(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    SecDurm=np.mean(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    FirstDursm.append(FirstDurm)
    SecDursm.append(SecDurm)
    FirstDur=np.sum(Flows_t.loc[Flows_t.DIP=="10.239.51.1","Curr"])
    SecDur=np.sum(Flows_t.loc[Flows_t.SIP=="10.239.51.1","Curr"])
    FirstDurs.append(FirstDur)
    SecDurs.append(SecDur)

plt.plot(Time,Firstconns, label="In-stream")
plt.plot(Time,Secconns, label="Out-stream")
plt.title("#Connections, 240cl/50s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstIPs, label="In-stream")
plt.plot(Time,SecIPs, label="Out-stream")
plt.title("#IPs, 240cl/50s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytes, label="In-stream")
plt.plot(Time,SecBytes, label="Out-stream")
plt.title("#Bytes, 240cl/50s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstBytesm, label="In-stream")
plt.plot(Time,SecBytesm, label="Out-stream")
plt.title("average bytes per connection, 240cl/50s")
plt.xlabel("Minutes")
plt.legend()
plt.show()
plt.plot(Time,FirstDursm, label="In-stream")
plt.plot(Time,SecDursm, label="Out-stream")
plt.title("average conn curation, 240cl/50s")
plt.xlabel("Minutes")
plt.legend()
plt.show()




Flows_network.LogBytes.hist()


########################################################################################################################
# Data_May
########################################################################################################################
filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.txt"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11_sample.txt"
filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22.txt"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22_sample.txt"
filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33.txt"
outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33_sample.txt"
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



