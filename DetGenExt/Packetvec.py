# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 13:54:47 2020

@author: henry
"""

from scapy.all import *

def payloadchecker(line):
    if (((line.name in ['IPv6','IP'])|(line.payload.name in ['IPv6','IP']))&(not(
                    ('ICMPv6 Neighbor' in line.payload.name)|
                    ('ICMPv6 Neighbor' in line.payload.payload.name)))):
        #iiiiii=1
        if line.payload.name in ['IPv6','IP']:
            line=line.payload
        if line.payload.name in ['TCP','UDP']:
            sport=str(line.payload.sport)
            dport=str(line.payload.dport)
        else:
            sport='-'
            dport='-'
        
        if line.payload.name!="TCP":
            sport=False
            dport=False
        return sport,dport
    else:
        return False, False


def Packetvector(filename):
    #pingpackets = rdpcap(filename)
    pingpackets = PcapReader(filename)
    #Compstats=open(outputfilename,"w")
    Pktnumber=0
    N=18
    IATs=[]
    Sizes=[]
    Flags=[]
    Dirs=[]
    
    Sport=None
    Dport=None
    
    for line in pingpackets:
        
        if line.name=="Ethernet":
            line=line.payload
        
        packettime=line.time
        sport,dport=payloadchecker(line)
        if sport==False:
                continue
        if Sport==None:
            Sport=sport
            Dport=dport
        if (Sport==sport)&(Dport==dport):
            Dir="S"
        elif (Dport==sport)&(Sport==dport):
            Dir="D"
        else:
            continue
        Pktnumber+=1
        
        Byte=int(line.len)
        Flag=str(line.payload.flags)
        #print(packettime)
        
        #print(Byte)
        
        IATs.extend([packettime])
        
        Sizes.extend([Byte])
        Flags.extend([Flag])
        Dirs.extend([Dir])
        print(Pktnumber)
        if Pktnumber>=N:
            print("N")
            return IATs,Sizes,Flags,Dirs


filename="Desktop/PhD_project/dump-050-vsftpd-server-2019-08-02_11-02-33-sc6-1.pcap"

filename1="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-1.pcap"
filename2="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-2.pcap"
filename3="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-3.pcap"

filename4="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-1.pcap"
filename5="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-2.pcap"
filename6="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-3.pcap"


filenames=[filename1,filename2,filename3]

IATss=[]
Sizess=[]
Flagss=[]
Dirss=[]
for filename in filenames:
    IATs,Sizes,Flags,Dirs=Packetvector(filename)
    IATss.extend(IATs)
    Sizess.extend(Sizes)
    Flagss.extend(Flags)
    Dirss.extend(Dirs)
    
    