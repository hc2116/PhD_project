#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
from Desktop.PhD_project.BT.Flowfunctions.flowfunctions2 import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
from Desktop.PhD_project.DetGenExt.Extension_paper.src.Flowfunctions.flowfunctions import *

from Desktop.PhD_project.DetGenExt.Extension_paper.src.Flowfunctions.flowfunctions import *


filename="Desktop/PhD_project/BT/Data_Adi/stepping-stone-randomIPs.pcap"
filename="Desktop/PhD_project/DetGenExt/Extension_paper/src/dump-050-vsftpd-server-2019-08-02_11-02-33-sc6-1.pcap"
filename="Desktop/PhD_project/DetGenExt/Extension_paper/src/noise51_relay_stepstone-2019-11-29_18-57-53-sc1-1.pcap"
filename="Desktop/PhD_project/Data/CIC/Friday-WorkingHours.pcap"
outputfilename="Desktop/PhD_project/Data/CIC/Friday-WorkingHoursTest.txt"

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
Flows.iloc[:,44:64].head()
Flows.iloc[:,64:84].head()
Flows.iloc[:84:104].head()
Flows.iloc[:,104:124].head()
Flows.iloc[:,124:144].head()
Flows.iloc[:,144:164].head()

Flows.SYN2.sum()
Flows.shape



81101-80841
