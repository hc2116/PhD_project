#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""
import os
from scapy.all import *
import re
from Desktop.Project.Flow_Clustering_2nd_attempt.flowfunctions import Vardecl, writeflow, Compflows, Compflowstxt
from Desktop.Project.Flow_Clustering_2nd_attempt.flowfunctions2 import Vardeclpcap, Compflowspcap

filename="Desktop/Project/Flow_Clustering_2nd_attempt/dump-011-ping2-2018-08-07-1732.pcap"
filename="Desktop/Project/Flow_Clustering_2nd_attempt/tcptest.pcap"

Compflows(filename,
          "Desktop/Project/Flow_Clustering_2nd_attempt/Flows4.txt",
          pcap=True)

try:
    os.remove("Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt")
except OSError:
    pass

Packets = open("Desktop/Project/Data/ImpactRep/Random/Packets2")
Compflows=open("Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt","w")

#Packets = open("Desktop/Project/Flow_Clustering_2nd_attempt/textcon.txt")


line=Packets.readline().split('","')

while line[4]!="TCP" or ("Packet size limited" in line[6]):
    line=Packets.readline().split('","')
a=line[6].split(" ")
Dict=[line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4]]

Flowd={}
Vars=[]

import re
from Desktop.Project.Flow_Clustering_2nd_attempt.flowfunctions import Vardecl, writeflow

Vardecl(line,Dict,Flowd,Vars,Init=True)

linestr="SIP,DIP,Prot,SPort,DPort"
for aa in Vars:
    if not ("temp" in aa):
        linestr+=","+aa
linestr+="\n"

Compflows.write(linestr)

limiter=0
limiter2=0
timeout=500
nbulks=1
idletime=4

for lin in Packets:
    #print(line)
    #lin=Packets.readline()
    line=lin.split('","')
    
    if line[4]=="TCP" and (not "Packet size limited" in line[6]):
        if line[6][0]=="[":
            line[6]=re.sub(r'.*?] ', '', line[6],1)
        if line[6][0]=="[":
            line[6]=re.sub(r'.*?] ', '', line[6],1)
        a=line[6].split(" ")
        # Test if direct connection is in Dict ###############################################
        if line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4] in Dict:
            index=Dict.index(line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4])
            # Bytes ###############################################
            SByte=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            Flowd["SBytes"][index]+=SByte
            Flowd["SBytes_std"][index]+=SByte**2
            Flowd["SBytes_max"][index]=max([Flowd["SBytes_max"][index],SByte])
            Flowd["NSPack"][index]+=1
            # Time ###############################################
            Interarr=float(line[1])-Flowd["Curr"][index]
            Flowd["Curr"][index]=float(line[1])
            Flowd["Inter_std"][index]+=Interarr**2
            Flowd["Inter_max"][index]=max([Flowd["Inter_max"][index],Interarr])
            if Interarr>idletime:
                Flowd["NIdle"][index]+=1
                Flowd["tIdle"][index]+=Interarr
                Flowd["tIdle_std"][index]+=Interarr**2
                
          # Test for Bulk mode ###############################################
            # Test if in bulk currently ###############################################
            if Flowd["B_Ind_temp"][index]==1:
                Flowd["B_IndP_temp"][index]+=1
                Flowd["B_Packets_temp"][index]+=1
                Flowd["B_Bytes_temp"][index]+=SByte
                Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
            # Otherwise delete previous params ###############################################
            elif Flowd["B_Packets_temp"][index]>3:
                # Add transaction mode ###############################################
                if Flowd["T_Ind"][index]==True:
                    Flowd["T_Counter"][index]+=1
                    Flowd["T_Packets_max"][index]=max([Flowd["T_Packets_max"][index],Flowd["T_Packets_temp"][index]])
                    Flowd["T_Bytes_max"][index]=max([Flowd["T_Bytes_max"][index],Flowd["T_Bytes_temp"][index]])
                    Flowd["T_Dur_max"][index]=max([Flowd["T_Dur_max"][index],Flowd["T_Dur_temp"][index]])
                    Flowd["T_Packets_temp"][index]=1
                    Flowd["T_Bytes_temp"][index]=SByte
                    Flowd["T_Dur_temp"][index]=0
                    Flowd["T_Ind"][index]=False
                # Add bulk mode ###############################################
                Flowd["B_Counter"][index]+=1
                Flowd["B_Packets"][index]+=Flowd["B_Packets_temp"][index]
                Flowd["B_Bytes"][index]+=Flowd["B_Bytes_temp"][index]
                Flowd["B_Dur"][index]+=Flowd["B_Dur_temp"][index]
                Flowd["B_Packets_max"][index]=max([Flowd["B_Packets_max"][index],Flowd["B_Packets_temp"][index]])
                Flowd["B_Bytes_max"][index]=max([Flowd["B_Bytes_max"][index],Flowd["B_Bytes_temp"][index]])
                Flowd["B_Dur_max"][index]=max([Flowd["B_Dur_max"][index],Flowd["B_Dur_temp"][index]])
                Flowd["B_Ind"][index]+=Flowd["B_Ind_temp"][index]
                Flowd["B_IndP"][index]+=Flowd["B_IndP_temp"][index]
                # Add first bulks ###############################################
                if Flowd["B_Counter"][index]<=nbulks:
                    BC=str(Flowd["B_Counter"][index])
                    Flowd[BC+"B_Packets"][index]=Flowd["B_Packets_temp"][index]
                    Flowd[BC+"B_Bytes"][index]=Flowd["B_Bytes_temp"][index]
                    Flowd[BC+"B_Dur"][index]=Flowd["B_Dur_temp"][index]
                    Flowd[BC+"B_Ind"][index]=Flowd["B_Ind_temp"][index]
                # To do
                Flowd["B_Packets_temp"][index]=1
                Flowd["B_Bytes_temp"][index]=SByte
                Flowd["B_Dur_temp"][index]=0
                Flowd["B_Ind_temp"][index]=1
                Flowd["B_IndP_temp"][index]=1
            else:
                Flowd["T_Packets_temp"][index]+=Flowd["B_Packets_temp"][index]
                if Flowd["T_Packets_temp"][index]>3&Flowd["T_Ind"][index]==False:
                    Flowd["T_Ind"][index]=True
                Flowd["T_Bytes_temp"][index]+=Flowd["B_Bytes_temp"][index]+SByte
                Flowd["T_Dur_temp"][index]+=Flowd["B_Dur_temp"][index]+Interarr
                Flowd["B_Packets_temp"][index]=1
                Flowd["B_Bytes_temp"][index]=SByte
                Flowd["B_Dur_temp"][index]=0
                Flowd["B_Ind_temp"][index]=1
                Flowd["B_IndP_temp"][index]=1
                     
            # Test for FIN flag ###############################################
            if  Flowd["FIN1"][index]==False and "FIN" in line[6]:
                Flowd["FIN1"][index]=True
                Flowd["FIN_init"][index]=1
            elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and "FIN" in line[6]:
                Flowd["FIN2"][index]=True
            elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==True and "ACK" in line[6]:
                writeflow(index,Flowd,Dict,Vars,Compflows)
            
        # Test if reverse connection is in Dict ###############################################
        elif line[3]+","+line[2]+","+line[4]+","+a[4]+a[2]+a[0] in Dict:            
            index=Dict.index(line[3]+","+line[2]+","+line[4]+","+a[4]+a[2]+a[0])

            # Test for SYN flag ###############################################
            if Flowd["NSPack"][index]==1&(Flowd["NDPack"][index]==0)&Flowd["SYN1"][index]==True:                        
                Flowd["SYN2"][index]="SYN" in line[6]
                #print("SYN", str("SYN" in line[6]),str(Flowd["SYN2"][index]))

            #Flowd["DBytes"][index]+=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            DByte=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            Flowd["DBytes"][index]+=DByte
            Flowd["DBytes_std"][index]+=DByte**2
            Flowd["DBytes_max"][index]=max([Flowd["DBytes_max"][index],DByte])
            Flowd["NDPack"][index]+=1
            Interarr=float(line[1])-Flowd["Curr"][index]
            Flowd["Curr"][index]=float(line[1])
            Flowd["Inter_std"][index]+=Interarr**2
            Flowd["Inter_max"][index]=max([Flowd["Inter_max"][index],Interarr])
            if Interarr>idletime:
                Flowd["NIdle"][index]+=1
                Flowd["tIdle"][index]+=Interarr
                       
            # Test for Bulk mode ###############################################
            # Test if in bulk currently ###############################################
            if Flowd["B_Ind_temp"][index]==2:
                Flowd["B_Packets_temp"][index]+=1
                Flowd["B_IndP_temp"][index]+=2
                Flowd["B_Bytes_temp"][index]+=DByte
                Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
            # Otherwise delete previous params ###############################################
            elif Flowd["B_Packets_temp"][index]>3:
                # Add transaction mode ###############################################
                if Flowd["T_Ind"][index]==True:
                    Flowd["T_Counter"][index]+=1
                    Flowd["T_Packets_max"][index]=max([Flowd["T_Packets_max"][index],Flowd["T_Packets_temp"][index]])
                    Flowd["T_Bytes_max"][index]=max([Flowd["T_Bytes_max"][index],Flowd["T_Bytes_temp"][index]])
                    Flowd["T_Dur_max"][index]=max([Flowd["T_Dur_max"][index],Flowd["T_Dur_temp"][index]])
                    Flowd["T_Packets_temp"][index]=1
                    Flowd["T_Bytes_temp"][index]=DByte
                    Flowd["T_Dur_temp"][index]=0
                    Flowd["T_Ind"][index]=False
                # Add bulk mode ###############################################
                Flowd["B_Counter"][index]+=1
                Flowd["B_Packets"][index]+=Flowd["B_Packets_temp"][index]
                Flowd["B_Bytes"][index]+=Flowd["B_Bytes_temp"][index]
                Flowd["B_Dur"][index]+=Flowd["B_Dur_temp"][index]
                Flowd["B_Packets_max"][index]=max([Flowd["B_Packets_max"][index],Flowd["B_Packets_temp"][index]])
                Flowd["B_Bytes_max"][index]=max([Flowd["B_Bytes_max"][index],Flowd["B_Bytes_temp"][index]])
                Flowd["B_Dur_max"][index]=max([Flowd["B_Dur_max"][index],Flowd["B_Dur_temp"][index]])
                Flowd["B_Ind"][index]+=Flowd["B_Ind_temp"][index]
                Flowd["B_IndP"][index]+=Flowd["B_IndP_temp"][index]
                # Add first bulks ###############################################
                if Flowd["B_Counter"][index]<=nbulks:
                    BC=str(Flowd["B_Counter"][index])
                    Flowd[BC+"B_Packets"][index]=Flowd["B_Packets_temp"][index]
                    Flowd[BC+"B_Bytes"][index]=Flowd["B_Bytes_temp"][index]
                    Flowd[BC+"B_Dur"][index]=Flowd["B_Dur_temp"][index]
                    Flowd[BC+"B_Ind"][index]=Flowd["B_Ind_temp"][index]
                # To do
                Flowd["B_Packets_temp"][index]=1
                Flowd["B_Bytes_temp"][index]=SByte
                Flowd["B_Dur_temp"][index]=0
                Flowd["B_Ind_temp"][index]=2
                Flowd["B_IndP_temp"][index]=2
            else:
                Flowd["T_Packets_temp"][index]+=Flowd["B_Packets_temp"][index]
                if Flowd["T_Packets_temp"][index]>3&Flowd["T_Ind"][index]==False:
                    Flowd["T_Ind"][index]=True
                Flowd["T_Bytes_temp"][index]+=Flowd["B_Bytes_temp"][index]+DByte
                Flowd["T_Dur_temp"][index]+=Flowd["B_Dur_temp"][index]+Interarr
                Flowd["B_Packets_temp"][index]=1
                Flowd["B_Bytes_temp"][index]=DByte
                Flowd["B_Dur_temp"][index]=0
                Flowd["B_Ind_temp"][index]=2
                Flowd["B_IndP_temp"][index]=2
                
            # Test for FIN flag ###############################################
            if  Flowd["FIN1"][index]==False and "FIN" in line[6]:
                Flowd["FIN1"][index]=True
                Flowd["FIN_init"][index]=2
            elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and "FIN" in line[6]:
                Flowd["FIN2"][index]=True
            elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==True and "ACK" in line[6]:
                writeflow(index,Flowd,Dict,Vars,Compflows)
                
#Flowd,lin
        # Write connection to Dict ###############################################
        else:
            Dict.append(",".join(line[2:5])+","+a[0]+a[2]+a[4])
            Vardecl(line,Dict,Flowd,[],Init=False)
    
    limiter+=1
    limiter2+=1
    if limiter==100000:
        print("Iterations:",limiter2)
        print("Dictionary length:",len(Dict))
        limiter=0
        curtime=float(line[1])
        for ii in reversed(range(len(Dict))):
            if (curtime-Flowd["Curr"][ii])>timeout:
                writeflow(ii,Flowd,Dict,Vars,Compflows)

            
for ii in reversed(range(len(Dict))):
    writeflow(ii,Flowd,Dict,Vars,Compflows)

Packets.close()
Compflows.close()



###################################################################################
# =============================================================================
# Packets.close()
# Packets = open("Desktop/Project/Flow_Clustering_2nd_attempt/Packets2")
# testing=True
# 
# while  testing:
#     lin=Packets.readline()
#     line=lin.split('","')
#     if "TSval" in line[6]:
#         print(line)
#         testing=False
#         
# 
# 
# 'fasdf asdfadf"asdfasdf'.replace('"',' ').split(' ')
# stri='[TCP ACKed unseen segment] 524  >  1077 [ACK] Seq=88053022 Ack=13369719 Win=20144 Len=1460"\n'
# re.sub(r'.*?] ', '', stri,1)
# 
# =============================================================================
