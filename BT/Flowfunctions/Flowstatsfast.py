#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
from Desktop.PhD_project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.PhD_project.BT.Flowfunctions.flowfunctions import *

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



81101-80841
