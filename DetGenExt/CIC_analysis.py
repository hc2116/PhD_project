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

NPackets=Mondayflows.loc[:,[" Destination Port"," Total Fwd Packets"]].groupby([" Destination Port"]).sum()

TotalL=Mondayflows.loc[:,[" Destination Port","Total Length of Fwd Packets"]].groupby([" Destination Port"]).sum()

TotalLL=TotalL.join(NPackets)

#TotalLL=TotalL.merge(NPackets,how='inner', on=' Destination Port')

TotalLLL=TotalLL.join(FreqPort).sort_values(by="Total Length of Fwd Packets",ascending=False)

TotalLLL=TotalLL.join(FreqPort).sort_values(by=" Total Fwd Packets",ascending=False)

TotalLLL
 