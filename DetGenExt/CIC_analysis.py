# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:48:41 2021

@author: henry
"""

import pandas as pd

Mondayflows=pd.read_csv("Desktop/PhD_project/Data/CIC/Monday-WorkingHours.pcap_ISCX.csv")


Mondayflows.columns


FreqPort=Mondayflows.loc[:," Destination Port"].value_counts()/len(Mondayflows.loc[:," Destination Port"])
FreqPort.name="Frequency"

NPackets=Mondayflows.loc[:,[" Destination Port"," Total Fwd Packets"]].groupby([" Destination Port"]).mean()

TotalL=Mondayflows.loc[:,[" Destination Port","Total Length of Fwd Packets"]].groupby([" Destination Port"]).mean()

TotalLL=TotalL.join(NPackets)

#TotalLL=TotalL.merge(NPackets,how='inner', on=' Destination Port')

TotalLLL=TotalLL.join(FreqPort).sort_values(by="Total Length of Fwd Packets",ascending=False)

TotalLLL=TotalLL.join(FreqPort).sort_values(by=" Total Fwd Packets",ascending=False)

TotalLLL=TotalLL.join(FreqPort).sort_values(by="Frequency",ascending=False)

TotalLLL


########################################################################

import pandas as pd 

HTTP_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-021-nginxWget-2021-03-02_17-48-27-labels.csv")
SSH_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-090-openssh-2021-02-18_21-53-46-labels.csv")

SSH_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-090-openssh-2021-03-10_19-13-15-labels.csv",delimiter=";")