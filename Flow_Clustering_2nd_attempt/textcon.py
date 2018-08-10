#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 15:24:07 2018

@author: henry
"""

Packets = open("Desktop/Project/Flow_Clustering_2nd_attempt/Packets2")
textcon=open("Desktop/Project/Flow_Clustering_2nd_attempt/textcon.txt","w")


# =============================================================================
# lin=Packets.readline()
# line=lin.split('","')
# =============================================================================

i=0
for lin in Packets:
    i+=1
    line=lin.split('","')

    if ('131.243.141.141' in line[2:4])&('208.189.11.184' in line[2:4])&('1525' in line[6]):
        textcon.write(lin)
    if i%100000==0:
        print(i)


Packets.close()
textcon.close()


# =============================================================================
# =============================================================================
# =============================================================================
filename="Desktop/Project/Data/UNSW/1.pcap"
pingpackets = PcapReader(filename)

counter=0
firstlayerprot=[]
seclayerprot=[]
thirdlayerprot=[]
for line in pingpackets:
    counter+=1
    if not (line.name  in firstlayerprot):
        firstlayerprot.append(line.name)
    if not (line.payload.name  in seclayerprot):
        seclayerprot.append(line.payload.name)
    if not (line.payload.payload.name  in thirdlayerprot):
        thirdlayerprot.append(line.payload.payload.name)