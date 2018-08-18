#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
from scapy.all import *
import re
from Desktop.Project.Flow_Clustering_2nd_attempt.flowfunctions import Vardecl, writeflow, Flowcomp, Compflowstxt, Vardeclpcap, Compflowspcap
import Desktop.Project.Flow_Clustering_2nd_attempt.flowfunctions

filename="Desktop/Project/Flow_Clustering_2nd_attempt/dump-011-ping2-2018-08-07-1732.pcap"
filename="Desktop/Project/Flow_Clustering_2nd_attempt/tcptest.pcap"
outputfilename="Desktop/Project/Flow_Clustering_2nd_attempt/Flows4.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)



filename="Desktop/Project/Data/UNSW/1.pcap"
filename="Desktop/Project/Flow_Clustering_2nd_attempt/tcptest.pcap"
outputfilename="Desktop/Project/Flow_Clustering_2nd_attempt/FlowsUNSW1.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)



filename="Desktop/Project/Data/UNSW/1.pcap"
filename="Desktop/Project/Flow_Clustering_2nd_attempt/tcptest.pcap"
outputfilename="Desktop/Project/Flow_Clustering_2nd_attempt/FlowsUNSW1.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)




>>>>>>> e479d64d0a38b7cb84ef1c8414c2f1404a766596
filename="Desktop/Project/Data/CIC/Monday-WorkingHours.pcap"
outputfilename="Desktop/Project/Flow_Clustering_2nd_attempt/FlowsCIC.txt"

Flowcomp(filename,
          outputfilename,
          pcap=True)


packets[1].summary()
packets[1].show()

packets[1].payload.payload.len

packets=rdpcap(filename)


print(packets[1])

print((packets[1].payload))

packets[1]
print(str(packets[1].payload.len))

line=packets[99]

