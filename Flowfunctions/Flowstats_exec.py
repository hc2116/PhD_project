#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
from Desktop.PhD_project.Flowfunctions.flowfunctions import *


filename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs.pcap"
outputfilename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs_flow.txt"
outputfilename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs_flow2.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)

import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 20) 
Flows=pd.read_csv("Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs_flow2.txt")


Flows.Prot.value_counts()
Flows.SIP.value_counts()
Flows.DIP.value_counts()


Flows.iloc[:,4:24].head()
Flows.iloc[:,24:44].head()
Flows.iloc[:,44:64].head()
Flows.iloc[:,64:84].head()
Flows.iloc[:84:104].head()
Flows.iloc[:,104:124].head()
Flows.iloc[:,124:144].head()
Flows.iloc[:,144:164].head()

Flows.SYN2.sum()
Flows.shape

Flows.loc[Flows.SIP=="10.239.159.45",:].DIP.value_counts()

Flows.loc[Flows.SIP=="10.239.27.120",:].DIP.value_counts()

Flows.loc[Flows.SIP=="10.239.239.235",:].DIP.value_counts()


Flows.DPort.value_counts()


Flows.loc[Flows.DPort==80,:].SBytes.hist()
Flows.loc[Flows.DPort==80,:].DBytes.hist()

Flows.loc[Flows.DPort==3128,:].SBytes.hist()
Flows.loc[Flows.DPort==3128,:].DBytes.hist()


Flows.loc[Flows.DPort==3128,:].SBytes.value_counts()
Flows.loc[Flows.DPort==3128,:].DBytes.value_counts()

Flows.loc[Flows.DPort==80,:].SBytes.value_counts()
Flows.loc[Flows.DPort==80,:].DBytes.value_counts()

Flows.loc[Flows.DPort==80,:].NPack.hist()
Flows.loc[Flows.DPort==3128,:].NPack.hist()



Flows.loc[Flows.DPort==3128,:].Inter.hist()
Flows.loc[Flows.DPort==80,:].Inter.hist()

Flows.loc[Flows.DPort==80,:].Inter_av
Flows.loc[Flows.DPort==3128,:].Inter_av.mean()

Flows.loc[Flows.DPort==80,:].SBytes.value_counts()
Flows.loc[Flows.DPort==80,:].DBytes.value_counts()

Flows.loc[Flows.DPort==80,:].NPack.hist()
Flows.loc[Flows.DPort==3128,:].NPack.hist()







Flows.DPort

np.log(Flows.SBytes).hist()

np.log(Flows.DBytes).hist()
Flows.SBytes.unique()

np.median(Flows.DBytes)
max(Flows.SBytes)


Flows.Inter.hist()

Flows.Inter


max(pd.to_datetime(Flows.Curr,unit='s'))


Flows.Curr.to_datetime()


81101-80841

Flows.SIP=="10.239.159.45"
