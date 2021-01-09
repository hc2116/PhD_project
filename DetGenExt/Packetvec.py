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
    N=40
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
            print(dport)
            if dport=="45261":
                Sport=sport
                Dport=dport
            else:
                continue
        if (Sport==sport)&(Dport==dport):
            Dir="Forward"
        elif (Dport==sport)&(Sport==dport):
            Dir="Backward"
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



def Packetvector2(filename,outputfile,Port):
    #pingpackets = rdpcap(filename)
    pingpackets = PcapReader(filename)
    #Compstats=open(outputfilename,"w")
    Pktnumber=0
#    N=40
    IATs=[]
    Sizes=[]
    Flags=[]
    Dirs=[]
    f = open(outputfile, "w")
    f.write("SPort,DPort,Time,Size,Flag,Dir\n")
    
    for line in pingpackets:
        
        if line.name=="Ethernet":
            line=line.payload
        
        packettime=line.time
        sport,dport=payloadchecker(line)
        if sport==False:
                continue
        if dport==str(Port):
            Dir="Forward"
            Sport=sport
            Dport=dport
        elif sport==str(Port):
            Dir="Backward"
            Sport=dport
            Dport=sport
        else:
            continue
        Pktnumber+=1
        
        Byte=int(line.len)
        Flag=str(line.payload.flags)
        f.write(str(Sport)+","+str(Dport)+","+str(packettime)+","+str(Byte)+","+str(Flag)+","+str(Dir)+"\n")
    f.close()
    return IATs,Sizes,Flags,Dirs




filename="Desktop/PhD_project/dump-050-vsftpd-server-2019-08-02_11-02-33-sc6-1.pcap"

filename1="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-1.pcap"
filename2="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-2.pcap"
filename3="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-05-41-3.pcap"

filename4="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-1.pcap"
filename5="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-2.pcap"
filename6="Desktop/Ubuntu_Files/dump-090-sshd-client-sc1-2020-10-05_19-09-09-3.pcap"


filenames=[filename4,filename5,filename6]

filename1="Desktop/Ubuntu_Files/dump-050-vsftpd-client-2020-10-02_17-35-18-sc1-1.pcap"
filename2="Desktop/Ubuntu_Files/dump-050-vsftpd-server-2020-10-02_17-35-18-sc1-1.pcap"

filename1="Desktop/Ubuntu_Files/dump-150-attacker-2021-01-07_12-59-52-1.pcap"


filename1="Desktop/Ubuntu_Files/dump-150-attacker-2021-01-07_12-59-52-1.pcap"
IATs,Sizes,Flags,Dirs=Packetvector2(filename1,"Desktop/SQL_traffic.txt",80)

filename1="Desktop/Ubuntu_Files/dump-150-sql-2021-01-07_15-54-03-1.pcap"
IATs,Sizes,Flags,Dirs=Packetvector2(filename1,"Desktop/SQL_traffic3.txt",3306)

filename1="Desktop/Ubuntu_Files/firefox.pcapng"
IATs,Sizes,Flags,Dirs=Packetvector2(filename1,"Desktop/firefox.txt",443)



filenames=[filename1,filename2]

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
    
IATss
Sizess
Flagss
Dirss
    