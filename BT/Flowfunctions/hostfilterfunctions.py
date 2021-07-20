#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:27:14 2018

@author: henry
"""
import re
import math as mt
from scapy.all import *
import random 
from datetime import datetime
import pandas as pd


# CICIDS

Hosts=["192.168.10.3","192.168.10.50","192.168.10.51","192.168.10.19","192.168.10.9","192.168.10.25"]
#
#filename="Desktop/Project/Data/CIC/Friday-WorkingHours.pcap"
#outputfilename="Desktop/Project/Data/CIC/Friday-WorkingHours_activity.csv"
#packetstats(filename,outputfilename,Hosts,5*60)
#output=pd.read_csv(outputfilename)

def packetstats(filename,outputfilename,Hosts,timeintervals,sample=False):
    inputpackets = PcapReader(filename)
    outputfile=open(outputfilename,"w")
    statsvector=statswriter(Hosts,outputfile)
    Timeinterval=0
    npackets=0
    messageprintcounter=100
    sample_rate=1000
    for line in inputpackets:
        pkttime=line.time
        if line.name=="Ethernet":
            line=line.payload
        if line.name!="IP":
            continue
        if sample==True:
            flip = random.randint(1, sample_rate)
            if flip!=1:
                continue
        if npackets==0:
            print(secondstodatetime(pkttime))
            Timeinterval=pkttime
        npackets+=1
        if npackets%messageprintcounter==0:
            print("Packet number:"+str(npackets))
            if npackets==(10*messageprintcounter):
                messageprintcounter*=10
        ldst=line.dst
        lsrc=line.src           
        if ldst in Hosts:
            if pkttime>(Timeinterval+timeintervals):
                statsvector.reset(Timeinterval,outputfile)
                print(secondstodatetime(Timeinterval))
                Timeinterval+=timeintervals
            statsvector.incoming(curHost=ldst,Bytes=int(line.len),IPaddress=lsrc)
        if lsrc in Hosts:
            if pkttime>(Timeinterval+timeintervals):
                statsvector.reset(Timeinterval,outputfile)
                print(secondstodatetime(Timeinterval))
                Timeinterval+=timeintervals
            statsvector.outgoing(curHost=lsrc,Bytes=int(line.len),IPaddress=ldst)    
    statsvector.reset(Timeinterval,outputfile)
    inputpackets.close()
    outputfile.close()


class statswriter:
    def __init__(self,Hosts,outputfile):
        Stats=["Ninputpackets",
        "Noutputpackets",
        "inputbytes",
        "outputbytes",
        "inputuniqueIPs",
        "outputuniqueIPs"]
        self.Hosts=Hosts
        self.nHosts=len(Hosts)
        self.nStats=len(Stats)
        self.lengthVec=self.nStats*self.nHosts
        self.IPaddressinc=[]
        self.IPaddressout=[]
        Columnnames=[(item+"_") for item in Stats for i in range(self.nHosts)]
        Hosts2=(Hosts*self.nStats)
        Columnnames=[Columnnames[i]+Hosts2[i] for i in range(len(Columnnames))]
        outputfile.write(",".join(Columnnames)+",Time\n")
        self.statsvector=[0]*self.lengthVec
        del(Columnnames)
        del(Hosts2)
        #return statsvector 
    def reset(self,Time,outputfile):
        outputfile.write(",".join([str(x) for x in self.statsvector])+","+secondstodatetime(Time)+"\n")
        self.statsvector=[0]*self.lengthVec
        self.IPaddressinc=[]
        self.IPaddressout=[]
    def incoming(self,curHost,Bytes,IPaddress):
        indexHost=self.Hosts.index(curHost)
        #Packets
        self.statsvector[indexHost]+=1
        #Bytes
        self.statsvector[indexHost+(2*self.nHosts)]+=Bytes
        #Bytes
        if IPaddress not in self.IPaddressinc:
            self.statsvector[indexHost+(4*self.nHosts)]+=1
            self.IPaddressinc.append(IPaddress)
    def outgoing(self,curHost,Bytes,IPaddress):
        indexHost=self.Hosts.index(curHost)
        #Packets
        self.statsvector[indexHost+(1*self.nHosts)]+=1
        #Bytes
        self.statsvector[indexHost+(3*self.nHosts)]+=Bytes
        #Bytes
        if IPaddress not in self.IPaddressout:
            self.statsvector[indexHost+(5*self.nHosts)]+=1
            self.IPaddressout.append(IPaddress)
        
def secondstodatetime(Time):
    return datetime.fromtimestamp(Time).strftime("%A %B %d %Y %I:%M:%S")


# =============================================================================
# filename="Desktop/Project/Data/CIC/Friday-WorkingHours.pcap"
# outputfilename="Desktop/Project/Data/CIC/Friday-WorkingHours_activity.csv"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/Data/CIC/Friday-WorkingHours_activity_sampled.csv"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# 
# filename="Desktop/Project/Data/CIC/Monday-WorkingHours.pcap"
# outputfilename="Desktop/Project/Data/CIC/Monday-WorkingHours_activity.csv"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/Data/CIC/Monday-WorkingHours_activity_sampled.csv"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# 
# 
# filename="Desktop/Project/Data/CIC/Thursday-WorkingHours.pcap"
# outputfilename="Desktop/Project/Data/CIC/Thursday-WorkingHours_activity.csv"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/Data/CIC/Thursday-WorkingHours_activity_sampled.csv"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# 
# filename="Desktop/Project/Data/CIC/Tuesday-WorkingHours.pcap"
# outputfilename="Desktop/Project/Data/CIC/Tuesday-WorkingHours_activity.csv"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/Data/CIC/Tuesday-WorkingHours_activity_sampled.csv"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# 
# filename="Desktop/Project/Data/CIC/Wednesday-WorkingHours.pcap"
# outputfilename="Desktop/Project/Data/CIC/Wednesday-WorkingHours_activity.csv"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/Data/CIC/Wednesday-WorkingHours_activity_sampled.csv"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# =============================================================================



Hosts=["10.239.51.1"]
# =============================================================================
# 
# 
# filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.pcap"
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11.txt"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-11_sample.txt"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22.pcap"
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22.txt"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-22_sample.txt"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33.pcap"
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33.txt"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-33_sample.txt"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# 
# 
# filename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-merged.pcap"
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-merged.txt"
# packetstats(filename,outputfilename,Hosts,3*60)
# outputfilename="Desktop/Project/BT/Data_Adi/Data_May/Client-Server-run-merged_sample.txt"
# packetstats(filename,outputfilename,Hosts,3*60,sample=True)
# =============================================================================

#####################################################################################



Hosts=["10.239.51.1"]


#filename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-11.pcap"
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-11.txt"
#packetstats(filename,outputfilename,Hosts,3*60)
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-11_sample.txt"
#packetstats(filename,outputfilename,Hosts,3*60,sample=True)
#filename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-22.pcap"
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-22.txt"
#packetstats(filename,outputfilename,Hosts,3*60)
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-22_sample.txt"
#packetstats(filename,outputfilename,Hosts,3*60,sample=True)
#filename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-33.pcap"
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-33.txt"
#packetstats(filename,outputfilename,Hosts,3*60)
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-33_sample.txt"
#packetstats(filename,outputfilename,Hosts,3*60,sample=True)
#
#
#filename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-merged.pcap"
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-merged.txt"
#packetstats(filename,outputfilename,Hosts,3*60)
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Client-Server-Stepping-Stone-big-payloads-merged_sample.txt"
#packetstats(filename,outputfilename,Hosts,3*60,sample=True)
#
##################################################################################
#
#filename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged.pcap"
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged.txt"
#packetstats(filename,outputfilename,Hosts,3*60)
#outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged_sample.txt"
#packetstats(filename,outputfilename,Hosts,3*60,sample=True)


filename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged.pcap"
outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged_sample2.txt"
packetstats(filename,outputfilename,Hosts,3*60,sample=True)
outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged_sample3.txt"
packetstats(filename,outputfilename,Hosts,3*60,sample=True)
outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged_sample4.txt"
packetstats(filename,outputfilename,Hosts,3*60,sample=True)
outputfilename="Desktop/Project/BT/Data_Adi/Data_June/Temp_Merged_sample5.txt"
packetstats(filename,outputfilename,Hosts,3*60,sample=True)



#####################################################################################




# =============================================================================
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_05filtered.pcap"
# DstAddresses=[]
# SrcAddresses=[]
# outputpackets = PcapReader(outputfilename)
# for line in outputpackets:
#     if line.dst not in DstAddresses:
#         DstAddresses.append(line.dst)
#     if line.src not in SrcAddresses:
#         SrcAddresses.append(line.src)
#     
#     if line.dst in SrcAddresses:
#         print(line.dst)
#     if line.src in DstAddresses:
#         print(line.src)
# outputpackets.close()
#     
# 
# 
#         
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130200.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_02filtered.pcap"
# 
#         
# def filterhostpackets(filename,outputfilename):
#     
#     inputpackets = PcapReader(filename)
#     pktdump = PcapWriter(outputfilename, append=False, sync=False)
#     print(filename)
#     nthpacket=0
#     IPaddresses=[]
#     messageprintcounter=100
#     
#     for line in inputpackets:
#         if line.name=="Ethernet":
#             line=line.payload
#         if line.name!="IP":
#             #print(line.name)
#             continue
#         if line.proto!=6:
#             #print(line.proto)
#             continue
#         ldst=line.dst
#         lsrc=line.src
#         
#         if nthpacket<100:
#             #print(line.time)
#             IPaddresses.append(ldst)
#             IPaddresses.append(line.src)
#             pktdump.write(line)
#         elif ldst in IPaddresses:
#             pktdump.write(line)
#         elif lsrc in IPaddresses:
#             pktdump.write(line)
#         nthpacket+=1
#         
#         if nthpacket%messageprintcounter==0:
#             print("Packet number:"+str(nthpacket))
#             if nthpacket==(10*messageprintcounter):
#                 messageprintcounter*=10
#         
#     pktdump.close()
#     inputpackets.close()
# 
#         
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130300.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_03filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130400.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_04filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130500.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_05filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# ############################################################################################
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130600.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_06filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130700.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_07filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130800.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_08filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-130900.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_09filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-131000.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_10filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-131100.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_11filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# 
# filename="Desktop/Project/Data/CAIDA/equinix-nyc.dirA.20190117-131200.UTC.anon.pcap"
# outputfilename="Desktop/Project/Data/CAIDA/2019_01_17_13_12filtered.pcap"
# 
# filterhostpackets(filename,outputfilename)
# 
# #from datetime import datetime
# #datetime.fromtimestamp(1547730060.000000).strftime("%A, %B %d, %Y %I:%M:%S")
# 
# =============================================================================
