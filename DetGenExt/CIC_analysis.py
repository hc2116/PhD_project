# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 11:48:41 2021

@author: henry
"""

import pandas as pd

Mondayflows=pd.read_csv("Desktop/PhD_project/Data/CIC/Monday-WorkingHours.pcap_ISCX.csv")
Tuesdayflows=pd.read_csv("Desktop/PhD_project/Data/CIC/Tuesday-WorkingHours.pcap_ISCX.csv")
Wednesdayflows=pd.read_csv("Desktop/PhD_project/Data/CIC/Wednesday-WorkingHours.pcap_ISCX.csv")
Thursdayflows1=pd.read_csv("Desktop/PhD_project/Data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv")
#Thursdayflows2=pd.read_csv("Desktop/PhD_project/Data/CIC/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv")
Thursdayflows3=pd.read_csv("Desktop/PhD_project/Data/CIC/Thursday-WorkingHours-Morning-WebAttacks_new.pcap_ISCX.csv")
#Thursdayflows4=pd.read_csv("Desktop/PhD_project/Data/CIC/Thursday-WorkingHours-Morning-WebAttacks2.pcap_ISCX.csv")
Fridayflows1=pd.read_csv("Desktop/PhD_project/Data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
Fridayflows2=pd.read_csv("Desktop/PhD_project/Data/CIC/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv")
Fridayflows3=pd.read_csv("Desktop/PhD_project/Data/CIC/Friday-WorkingHours-Morning.pcap_ISCX.csv")

Mondayflows=Mondayflows.append(Tuesdayflows)
Mondayflows=Mondayflows.append(Wednesdayflows)
Mondayflows=Mondayflows.append(Thursdayflows1)
Mondayflows=Mondayflows.append(Thursdayflows3)
Mondayflows=Mondayflows.append(Fridayflows1)
Mondayflows=Mondayflows.append(Fridayflows2)
Mondayflows=Mondayflows.append(Fridayflows3)

Mondayflows_old=Mondayflows
Mondayflows=Mondayflows.loc[Mondayflows.loc[:," Label"]=="BENIGN",:]

Mondayflows.columns
Mondayflows["Total Packets"]=Mondayflows.loc[:," Total Fwd Packets"]+Mondayflows.loc[:," Total Backward Packets"]
Mondayflows["Total Size"]=Mondayflows.loc[:,"Total Length of Fwd Packets"]+Mondayflows.loc[:,' Total Length of Bwd Packets']

FreqPort=Mondayflows.loc[:," Destination Port"].value_counts()/len(Mondayflows.loc[:," Destination Port"])
FreqPort.name="Frequency"


NPackets=Mondayflows.loc[:,[" Destination Port","Total Packets"]].groupby([" Destination Port"]).mean()
TotalL=Mondayflows.loc[:,[" Destination Port","Total Size"]].groupby([" Destination Port"]).mean()
NPackets.columns=["Mean Packets"]
TotalL.columns=["Mean size"]
TotalLL=TotalL.join(NPackets)

NPackets=Mondayflows.loc[:,[" Destination Port","Total Packets"]].groupby([" Destination Port"]).sum()
NPackets.columns=["Total Packets"]
TotalLL=TotalLL.join(NPackets)


TotalLLL=TotalLL.join(FreqPort).sort_values(by="Total Packets",ascending=False)
TotalLLL=TotalLL.join(FreqPort).sort_values(by="Frequency",ascending=False)


TotalLLL=TotalLL.sort_values(by="Total Packets",ascending=False)
TotalLLL["Total Packets Ratio"]=TotalLLL["Total Packets"]/TotalLLL["Total Packets"].sum()
TotalLLL.iloc[0:30,:].round(3)

TotalLLL.iloc[0:18,:].round(3)


########################################################################

import pandas as pd 

HTTP_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-021-nginxWget-2021-03-02_17-48-27-labels.csv")
SSH_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-090-openssh-2021-02-18_21-53-46-labels.csv")

SSH_labels=pd.read_csv("Desktop/Ubuntu_Files/capture-090-openssh-2021-03-10_19-13-15-labels.csv",delimiter=";")
