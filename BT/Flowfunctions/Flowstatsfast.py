#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
#from Desktop.PhD_project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.PhD_project.BT.Flowfunctions.flowfunctions import *

###############################################################################################################################
filename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs.pcap"
outputfilename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs_flow.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
pd.set_option('display.max_columns', 20)
Flows=pd.read_csv("Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs_flow.txt")


Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()


Flows.iloc[:,4:24].head()
Flows.iloc[:,24:44].head()

Flows.SYN2.sum()
Flows.shape


###############################################################################################################################
filename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new.pcap"
outputfilename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new_flow.txt"

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
filename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-100-server-new/stepping-stone-100clients-100server-new.pcap"
outputfilename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-100-server-new/stepping-stone-100clients-100server-new_flow.txt"
filename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new.pcap"
outputfilename="Desktop/PhD_project/BT/Data_Adi/Data_March/Stepping-Stone-1-server-new/stepping-stone-100clients-1server-new_flow.txt"


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

Flows.loc[Flows.SIP!="10.239.5","DIP"].value_counts()
Flows.loc[(Flows.SIP=="10.239.51.1")&(Flows.DIP!="10.239.51.1"),:]



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

plt.plot(Firstconns)
plt.plot(Secconns)
plt.show()
plt.plot(FirstIPs)
plt.plot(SecIPs)
plt.show()
plt.plot(FirstBytes)
plt.plot(SecBytes)
plt.show()
plt.plot(FirstBytesm)
plt.plot(SecBytesm)
plt.show()
plt.plot(FirstDursm)
plt.plot(SecDursm)
plt.show()




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
