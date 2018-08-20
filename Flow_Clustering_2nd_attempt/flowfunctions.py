#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:27:14 2018

@author: henry
"""
import re
from scapy.all import *

def Flowcomp(filename,outputfilename,pcap=True):
    if pcap==True:
        Compflowspcap(filename,outputfilename)
    else:
        Compflowstxt(filename,outputfilename)
        

def Compflowstxt(filename,outputfilename):
    Packets = open(filename)
    Compflows=open(outputfilename,"w")

    line=Packets.readline().split('","')

    while line[4]!="TCP" or ("Packet size limited" in line[6]):
        line=Packets.readline().split('","')
    a=line[6].split(" ")
    Dict=[line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4]]

    Flowd={}
    Vars=[]

    Vardecl(line,Dict,Flowd,Vars,Init=True,nbulks=nbulks)

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
                Vardecl(line,Dict,Flowd,[],Init=False,nbulks=nbulks)
    
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


def Compflowspcap(filename,outputfilename):
    #pingpackets = rdpcap(filename)
    Bulkpktn=3
    pingpackets = PcapReader(filename)
    Compflows=open(outputfilename,"w")
    #i=0
    iiiiii=0

    limiter=0
    limiter2=0
    timeout=500
    nbulks=8
    idletime=4    
    
    for line in pingpackets:
        if iiiiii==0:
            #print(str(line.name))
            #print(str(line.payload.name))
            #print(str(line.payload.len))
            if (((line.name in ['IPv6','IP'])|(line.payload.name in ['IPv6','IP']))&(not(
                    ('ICMPv6 Neighbor' in line.payload.name)|
                    ('ICMPv6 Neighbor' in line.payload.payload.name)))):
                iiiiii=1
                if line.payload.name in ['IPv6','IP']:
                    line=line.payload
                #print(str(line.name))
                if line.payload.name in ['TCP','UDP']:
                    sport=str(line.payload.sport)
                    dport=str(line.payload.dport)
                else:
                    sport='-'
                    dport='-'

                Dict=[str(line.src)+','+str(line.dst)+','+line.payload.name+','+sport+'>'+dport]
                Flowd={}
                Vars=[]

                Vardeclpcap(line,Dict,Flowd,Vars,Init=True,nbulks=nbulks)
                
                linestrvars="SIP,DIP,Prot,SPort,DPort"
                for aa in Vars:
                    if not ("temp" in aa):
                        linestrvars+=","+aa
                linestrvars+="\n"

                Compflows.write(linestrvars)

        
        elif (((line.name in ['IPv6','IP'])|(line.payload.name in ['IPv6','IP']))&(not(
                    ('ICMPv6 Neighbor' in line.payload.name)|
                    ('ICMPv6 Neighbor' in line.payload.payload.name)))):
            if line.payload.name in ['IPv6','IP']:
                line=line.payload
            
            if line.payload.name in ['TCP','UDP']:
                sport=str(line.payload.sport)
                dport=str(line.payload.dport)
            else:
                sport='-'
                dport='-'
            if str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport in Dict:
                index=Dict.index(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                # Bytes ###############################################
                SByte=int(line.len)
                Flowd["SBytes"][index]+=SByte
                Flowd["SBytes_std"][index]+=SByte**2
                Flowd["SBytes_max"][index]=max([Flowd["SBytes_max"][index],SByte])
                Flowd["NSPack"][index]+=1
                # Time ###############################################
                Interarr=float(line.time)-Flowd["Curr"][index]
                Flowd["Curr"][index]=float(line.time)
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
                    Flowd["T_assist_temp"][index]+=SByte
                    Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
                # Otherwise delete previous params ###############################################
                elif Flowd["B_Packets_temp"][index]>Bulkpktn:
                    # Add transaction mode ###############################################
                    if Flowd["T_Ind"][index]==True:
                        Flowd["T_Counter"][index]+=1
                        Flowd["T_Packets_max"][index]=max([Flowd["T_Packets_max"][index],Flowd["T_Packets_temp"][index]])
                        Flowd["T_Bytes_max"][index]=max([Flowd["T_Bytes_max"][index],Flowd["T_Bytes_temp"][index]])
                        Flowd["T_Dur_max"][index]=max([Flowd["T_Dur_max"][index],Flowd["T_Dur_temp"][index]])
                        #Flowd["T_Packets_temp"][index]=1
                        #Flowd["T_Bytes_temp"][index]=SByte
                        #Flowd["T_Dur_temp"][index]=0
                        #Flowd["T_Ind"][index]=False
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
                    # Reinitialise params
                    Flowd["B_Packets_temp"][index]=1
                    Flowd["B_Bytes_temp"][index]=SByte
                    Flowd["B_Dur_temp"][index]=0
                    Flowd["B_Ind_temp"][index]=1
                    Flowd["B_IndP_temp"][index]=1
                    Flowd["T_Packets_temp"][index]=1
                    Flowd["T_Bytes_temp"][index]=SByte
                    Flowd["T_Dur_temp"][index]=0
                    Flowd["T_Ind"][index]=False
                else:
                    Flowd["T_Packets_temp"][index]+=Flowd["B_Packets_temp"][index]
                    if Flowd["T_Packets_temp"][index]>3&Flowd["T_Ind"][index]==False:
                        Flowd["T_Ind"][index]=True
                    Flowd["T_Bytes_temp"][index]+=+SByte+Flowd["T_assist_temp"][index]
                    Flowd["T_assist_temp"][index]=0
                    Flowd["T_Dur_temp"][index]+=Flowd["B_Dur_temp"][index]+Interarr
                    Flowd["B_Packets_temp"][index]=1
                    Flowd["B_Bytes_temp"][index]=SByte
                    Flowd["B_Dur_temp"][index]=0
                    Flowd["B_Ind_temp"][index]=1
                    Flowd["B_IndP_temp"][index]=1
                     
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    if  Flowd["FIN1"][index]==False and "F" in str(line.payload.flags):
                        Flowd["FIN1"][index]=True
                        Flowd["FIN_init"][index]=1
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and "F" in str(line.payload.flags):
                        Flowd["FIN2"][index]=True
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==True and "A" in str(line.payload.flags):
                        writeflow(index,Flowd,Dict,Vars,Compflows)
            
            # Test if reverse connection is in Dict ###############################################
            elif str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport in Dict:            
                index=Dict.index(str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport)

                # Test for SYN flag ###############################################
                if Flowd["NSPack"][index]==1&(Flowd["NDPack"][index]==0)&Flowd["SYN1"][index]==True:                        
                    Flowd["SYN2"][index]="S" in str(line.payload.flags)
                    #print("SYN", str("SYN" in line[6]),str(Flowd["SYN2"][index]))

                #Flowd["DBytes"][index]+=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
                DByte=int(line.len)
                Flowd["DBytes"][index]+=DByte
                Flowd["DBytes_std"][index]+=DByte**2
                Flowd["DBytes_max"][index]=max([Flowd["DBytes_max"][index],DByte])
                Flowd["NDPack"][index]+=1
                Interarr=float(line.time)-Flowd["Curr"][index]
                Flowd["Curr"][index]=float(line.time)
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
                    Flowd["T_assist_temp"][index]+=DByte
                    Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
                # Otherwise delete previous params ###############################################
                elif Flowd["B_Packets_temp"][index]>Bulkpktn:
                    # Add transaction mode ###############################################
                    if Flowd["T_Ind"][index]==True:
                        Flowd["T_Counter"][index]+=1
                        Flowd["T_Packets_max"][index]=max([Flowd["T_Packets_max"][index],Flowd["T_Packets_temp"][index]])
                        Flowd["T_Bytes_max"][index]=max([Flowd["T_Bytes_max"][index],Flowd["T_Bytes_temp"][index]])
                        Flowd["T_Dur_max"][index]=max([Flowd["T_Dur_max"][index],Flowd["T_Dur_temp"][index]])
                        #Flowd["T_Packets_temp"][index]=1
                        #Flowd["T_Bytes_temp"][index]=DByte
                        #Flowd["T_Dur_temp"][index]=0
                        #Flowd["T_Ind"][index]=False
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
                    # Reinitialise params
                    Flowd["B_Packets_temp"][index]=1
                    Flowd["B_Bytes_temp"][index]=DByte
                    Flowd["B_Dur_temp"][index]=0
                    Flowd["B_Ind_temp"][index]=2
                    Flowd["B_IndP_temp"][index]=2
                    Flowd["T_Packets_temp"][index]=1
                    Flowd["T_Bytes_temp"][index]=DByte
                    Flowd["T_Dur_temp"][index]=0
                    Flowd["T_Ind"][index]=False
                else:
                    Flowd["T_Packets_temp"][index]+=Flowd["B_Packets_temp"][index]
                    if Flowd["T_Packets_temp"][index]>3&Flowd["T_Ind"][index]==False:
                        Flowd["T_Ind"][index]=True
                    Flowd["T_Bytes_temp"][index]+=+DByte+Flowd["T_assist_temp"][index]
                    Flowd["T_assist_temp"][index]=0
                    Flowd["T_Dur_temp"][index]+=Flowd["B_Dur_temp"][index]+Interarr
                    Flowd["B_Packets_temp"][index]=1
                    Flowd["B_Bytes_temp"][index]=DByte
                    Flowd["B_Dur_temp"][index]=0
                    Flowd["B_Ind_temp"][index]=2
                    Flowd["B_IndP_temp"][index]=2
                
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    if  Flowd["FIN1"][index]==False and "F" in str(line.payload.flags):
                        Flowd["FIN1"][index]=True
                        Flowd["FIN_init"][index]=2
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and "F" in str(line.payload.flags):
                        Flowd["FIN2"][index]=True
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==True and "A" in str(line.payload.flags):
                        writeflow(index,Flowd,Dict,Vars,Compflows)
                    
             #Flowd,lin
            # Write connection to Dict ###############################################    
            else:
                Dict.append(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                Vardeclpcap(line,Dict,Flowd,[],Init=False,nbulks=nbulks)
    
        limiter+=1
        limiter2+=1
        if limiter==100000:
            print("Iterations:",limiter2)
            print("Dictionary length:",len(Dict))
            limiter=0
            curtime=float(line.time)
            for ii in reversed(range(len(Dict))):
                if (curtime-Flowd["Curr"][ii])>timeout:
                    writeflow(ii,Flowd,Dict,Vars,Compflows)        
    for ii in reversed(range(len(Dict))):
        writeflow(ii,Flowd,Dict,Vars,Compflows) 
    #pingpackets.close()
    Compflows.close()

 
def Vardeclpcap(line,Dict,Flowd,Vars=[],Init=False,nbulks=8):   
    #Stats ######################################################
    if Init==True:
        Vars.append("SBytes")
        Flowd["SBytes"]=[]
    Flowd["SBytes"].append(int(line.len))
    if Init==True:
        Vars.append("SBytes_av")
        Flowd["SBytes_av"]=[]
    Flowd["SBytes_av"].append(0)
    if Init==True:
        Vars.append("DBytes")
        Flowd["DBytes"]=[]
    Flowd["DBytes"].append(0)
    if Init==True:
        Vars.append("DBytes_av")
        Flowd["DBytes_av"]=[]
    Flowd["DBytes_av"].append(0)
    if Init==True:
        Vars.append("SBytes_std")
        Flowd["SBytes_std"]=[]
    Flowd["SBytes_std"].append((int(line.len))**2)
    if Init==True:
        Vars.append("DBytes_std")
        Flowd["DBytes_std"]=[]
    Flowd["DBytes_std"].append(0)
    if Init==True:
        Vars.append("SBytes_max")
        Flowd["SBytes_max"]=[]
    Flowd["SBytes_max"].append(int(line.len))
    if Init==True:
        Vars.append("DBytes_max")
        Flowd["DBytes_max"]=[]
    Flowd["DBytes_max"].append(0)
    if Init==True:
        Vars.append("Start")
        Flowd["Start"]=[]
    Flowd["Start"].append(float(line.time))
    if Init==True:
        Vars.append("Curr")
        Flowd["Curr"]=[]
    Flowd["Curr"].append(float(line.time))
    if Init==True:
        Vars.append("Inter_av")
        Flowd["Inter_av"]=[]
    Flowd["Inter_av"].append(0)
    if Init==True:
        Vars.append("Inter_std")
        Flowd["Inter_std"]=[]
    Flowd["Inter_std"].append(0)
    if Init==True:
        Vars.append("Inter_max")
        Flowd["Inter_max"]=[]
    Flowd["Inter_max"].append(0)
    if Init==True:
        Vars.append("NIdle")
        Flowd["NIdle"]=[]
    Flowd["NIdle"].append(0)
    if Init==True:
        Vars.append("tIdle")
        Flowd["tIdle"]=[]
    Flowd["tIdle"].append(0)
    if Init==True:
        Vars.append("tIdle_av")
        Flowd["tIdle_av"]=[]
    Flowd["tIdle_av"].append(0)
    if Init==True:
        Vars.append("tIdle_std")
        Flowd["tIdle_std"]=[]
    Flowd["tIdle_std"].append(0)
    if Init==True:
        Vars.append("NSPack")
        Flowd["NSPack"]=[]
    Flowd["NSPack"].append(1)
    if Init==True:
        Vars.append("NDPack")
        Flowd["NDPack"]=[]
    Flowd["NDPack"].append(0)
    #SYN/FIN ######################################################
    if Init==True:
        Vars.append("SYN1")
        Flowd["SYN1"]=[]
    if line.payload.name=='TCP':    
        Flowd["SYN1"].append("S" in str(line.payload.flags))
    else: Flowd["SYN1"].append(False)
    if Init==True:
        Vars.append("SYN2")
        Flowd["SYN2"]=[]
    Flowd["SYN2"].append(False)
    if Init==True:
        Vars.append("FIN_init")
        Flowd["FIN_init"]=[]
    Flowd["FIN_init"].append(0)
    if Init==True:
        Vars.append("FIN1")
        Flowd["FIN1"]=[]
    Flowd["FIN1"].append(False)
    if Init==True:
        Vars.append("FIN2")
        Flowd["FIN2"]=[]
    Flowd["FIN2"].append(False)
    #Transaction mode ######################################################
    if Init==True:
        Vars.append("T_Ind")
        Flowd["T_Ind"]=[]
    Flowd["T_Ind"].append(False)
    if Init==True:
        Vars.append("T_Counter")
        Flowd["T_Counter"]=[]
    Flowd["T_Counter"].append(0)
    if Init==True:
        Vars.append("T_Packets_max")
        Flowd["T_Packets_max"]=[]
    Flowd["T_Packets_max"].append(0)
    if Init==True:
        Vars.append("T_Packets_temp")
        Flowd["T_Packets_temp"]=[]
    Flowd["T_Packets_temp"].append(1)
    if Init==True:
        Vars.append("T_Bytes_max")
        Flowd["T_Bytes_max"]=[]
    Flowd["T_Bytes_max"].append(0)
    if Init==True:
        Vars.append("T_Bytes_temp")
        Flowd["T_Bytes_temp"]=[]
    Flowd["T_Bytes_temp"].append(int(line.len))
    if Init==True:
        Vars.append("T_Dur_max")
        Flowd["T_Dur_max"]=[]
    Flowd["T_Dur_max"].append(0)
    if Init==True:
        Vars.append("T_Dur_temp")
        Flowd["T_Dur_temp"]=[]
    Flowd["T_Dur_temp"].append(0)
    if Init==True:
        Vars.append("T_assist_temp")
        Flowd["T_assist_temp"]=[]
    Flowd["T_assist_temp"].append(0)
    #Bulk mode ######################################################
    if Init==True:
        Vars.append("B_Counter")
        Flowd["B_Counter"]=[]
    Flowd["B_Counter"].append(0)
    if Init==True:
        Vars.append("B_Packets_temp")
        Flowd["B_Packets_temp"]=[]
    Flowd["B_Packets_temp"].append(1)
    if Init==True:
        Vars.append("B_Packets")
        Flowd["B_Packets"]=[]
    Flowd["B_Packets"].append(0)
    if Init==True:
        Vars.append("B_Packets_max")
        Flowd["B_Packets_max"]=[]
    Flowd["B_Packets_max"].append(0)
    if Init==True:
        Vars.append("B_Bytes_temp")
        Flowd["B_Bytes_temp"]=[]
    Flowd["B_Bytes_temp"].append(int(line.len))
    if Init==True:
        Vars.append("B_Bytes")
        Flowd["B_Bytes"]=[]
    Flowd["B_Bytes"].append(0)
    if Init==True:
        Vars.append("B_Bytes_max")
        Flowd["B_Bytes_max"]=[]
    Flowd["B_Bytes_max"].append(0)
    if Init==True:
        Vars.append("B_Dur_temp")
        Flowd["B_Dur_temp"]=[]
    Flowd["B_Dur_temp"].append(0)
    if Init==True:
        Vars.append("B_Dur")
        Flowd["B_Dur"]=[]
    Flowd["B_Dur"].append(0)
    if Init==True:
        Vars.append("B_Dur_max")
        Flowd["B_Dur_max"]=[]
    Flowd["B_Dur_max"].append(0)
    if Init==True:
        Vars.append("B_Ind")
        Flowd["B_Ind"]=[]
    Flowd["B_Ind"].append(0)
    if Init==True:
        Vars.append("B_IndP")
        Flowd["B_IndP"]=[]
    Flowd["B_IndP"].append(0)
    if Init==True:
        Vars.append("B_Ind_temp")
        Flowd["B_Ind_temp"]=[]
    Flowd["B_Ind_temp"].append(1)
    if Init==True:
        Vars.append("B_IndP_temp")
        Flowd["B_IndP_temp"]=[]
    Flowd["B_IndP_temp"].append(1)
    if Init==True:
        Vars.append("Perc_B")
        Flowd["Perc_B"]=[]
    Flowd["Perc_B"].append(0)
    #First Bulks######################################################
    for m in range(nbulks):
        BC=str(m+1)
        if Init==True:
            Vars.append(BC+"B_Packets")
            Flowd[BC+"B_Packets"]=[]
        Flowd[BC+"B_Packets"].append(0)
        if Init==True:
            Vars.append(BC+"B_Bytes")
            Flowd[BC+"B_Bytes"]=[]
        Flowd[BC+"B_Bytes"].append(0)
        if Init==True:
            Vars.append(BC+"B_Dur")
            Flowd[BC+"B_Dur"]=[]
        Flowd[BC+"B_Dur"].append(0)
        if Init==True:
            Vars.append(BC+"B_Ind")
            Flowd[BC+"B_Ind"]=[]
        Flowd[BC+"B_Ind"].append(1)
        
    


def Vardecl(line,Dict,Flowd,Vars=[],Init=False,nbulks=8):   
    #Stats ######################################################
    if Init==True:
        Vars.append("SBytes")
        Flowd["SBytes"]=[]
    Flowd["SBytes"].append(int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))
    if Init==True:
        Vars.append("SBytes_av")
        Flowd["SBytes_av"]=[]
    Flowd["SBytes_av"].append(0)
    if Init==True:
        Vars.append("DBytes")
        Flowd["DBytes"]=[]
    Flowd["DBytes"].append(0)
    if Init==True:
        Vars.append("DBytes_av")
        Flowd["DBytes_av"]=[]
    Flowd["DBytes_av"].append(0)
    if Init==True:
        Vars.append("SBytes_std")
        Flowd["SBytes_std"]=[]
    Flowd["SBytes_std"].append((int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))**2)
    if Init==True:
        Vars.append("DBytes_std")
        Flowd["DBytes_std"]=[]
    Flowd["DBytes_std"].append(0)
    if Init==True:
        Vars.append("SBytes_max")
        Flowd["SBytes_max"]=[]
    Flowd["SBytes_max"].append(int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))
    if Init==True:
        Vars.append("DBytes_max")
        Flowd["DBytes_max"]=[]
    Flowd["DBytes_max"].append(0)
    if Init==True:
        Vars.append("Start")
        Flowd["Start"]=[]
    Flowd["Start"].append(float(line[1]))
    if Init==True:
        Vars.append("Curr")
        Flowd["Curr"]=[]
    Flowd["Curr"].append(float(line[1]))
    if Init==True:
        Vars.append("Inter_av")
        Flowd["Inter_av"]=[]
    Flowd["Inter_av"].append(0)
    if Init==True:
        Vars.append("Inter_std")
        Flowd["Inter_std"]=[]
    Flowd["Inter_std"].append(0)
    if Init==True:
        Vars.append("Inter_max")
        Flowd["Inter_max"]=[]
    Flowd["Inter_max"].append(0)
    if Init==True:
        Vars.append("NIdle")
        Flowd["NIdle"]=[]
    Flowd["NIdle"].append(0)
    if Init==True:
        Vars.append("tIdle")
        Flowd["tIdle"]=[]
    Flowd["tIdle"].append(0)
    if Init==True:
        Vars.append("tIdle_av")
        Flowd["tIdle_av"]=[]
    Flowd["tIdle_av"].append(0)
    if Init==True:
        Vars.append("tIdle_std")
        Flowd["tIdle_std"]=[]
    Flowd["tIdle_std"].append(0)
    if Init==True:
        Vars.append("NSPack")
        Flowd["NSPack"]=[]
    Flowd["NSPack"].append(1)
    if Init==True:
        Vars.append("NDPack")
        Flowd["NDPack"]=[]
    Flowd["NDPack"].append(0)
    #SYN/FIN ######################################################
    if Init==True:
        Vars.append("SYN1")
        Flowd["SYN1"]=[]
    Flowd["SYN1"].append("SYN" in line[6])
    if Init==True:
        Vars.append("SYN2")
        Flowd["SYN2"]=[]
    Flowd["SYN2"].append(False)
    if Init==True:
        Vars.append("FIN_init")
        Flowd["FIN_init"]=[]
    Flowd["FIN_init"].append(0)
    if Init==True:
        Vars.append("FIN1")
        Flowd["FIN1"]=[]
    Flowd["FIN1"].append(False)
    if Init==True:
        Vars.append("FIN2")
        Flowd["FIN2"]=[]
    Flowd["FIN2"].append(False)
    #Transaction mode ######################################################
    if Init==True:
        Vars.append("T_Ind")
        Flowd["T_Ind"]=[]
    Flowd["T_Ind"].append(False)
    if Init==True:
        Vars.append("T_Counter")
        Flowd["T_Counter"]=[]
    Flowd["T_Counter"].append(0)
    if Init==True:
        Vars.append("T_Packets_max")
        Flowd["T_Packets_max"]=[]
    Flowd["T_Packets_max"].append(0)
    if Init==True:
        Vars.append("T_Packets_temp")
        Flowd["T_Packets_temp"]=[]
    Flowd["T_Packets_temp"].append(1)
    if Init==True:
        Vars.append("T_Bytes_max")
        Flowd["T_Bytes_max"]=[]
    Flowd["T_Bytes_max"].append(0)
    if Init==True:
        Vars.append("T_Bytes_temp")
        Flowd["T_Bytes_temp"]=[]
    Flowd["T_Bytes_temp"].append(int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))
    if Init==True:
        Vars.append("T_Dur_max")
        Flowd["T_Dur_max"]=[]
    Flowd["T_Dur_max"].append(0)
    if Init==True:
        Vars.append("T_Dur_temp")
        Flowd["T_Dur_temp"]=[]
    Flowd["T_Dur_temp"].append(0)
    #Bulk mode ######################################################
    if Init==True:
        Vars.append("B_Counter")
        Flowd["B_Counter"]=[]
    Flowd["B_Counter"].append(0)
    if Init==True:
        Vars.append("B_Packets_temp")
        Flowd["B_Packets_temp"]=[]
    Flowd["B_Packets_temp"].append(1)
    if Init==True:
        Vars.append("B_Packets")
        Flowd["B_Packets"]=[]
    Flowd["B_Packets"].append(0)
    if Init==True:
        Vars.append("B_Packets_max")
        Flowd["B_Packets_max"]=[]
    Flowd["B_Packets_max"].append(0)
    if Init==True:
        Vars.append("B_Bytes_temp")
        Flowd["B_Bytes_temp"]=[]
    Flowd["B_Bytes_temp"].append(0)
    if Init==True:
        Vars.append("B_Bytes")
        Flowd["B_Bytes"]=[]
    Flowd["B_Bytes"].append(0)
    if Init==True:
        Vars.append("B_Bytes_max")
        Flowd["B_Bytes_max"]=[]
    Flowd["B_Bytes_max"].append(0)
    if Init==True:
        Vars.append("B_Dur_temp")
        Flowd["B_Dur_temp"]=[]
    Flowd["B_Dur_temp"].append(0)
    if Init==True:
        Vars.append("B_Dur")
        Flowd["B_Dur"]=[]
    Flowd["B_Dur"].append(0)
    if Init==True:
        Vars.append("B_Dur_max")
        Flowd["B_Dur_max"]=[]
    Flowd["B_Dur_max"].append(0)
    if Init==True:
        Vars.append("B_Ind")
        Flowd["B_Ind"]=[]
    Flowd["B_Ind"].append(0)
    if Init==True:
        Vars.append("B_IndP")
        Flowd["B_IndP"]=[]
    Flowd["B_IndP"].append(0)
    if Init==True:
        Vars.append("B_Ind_temp")
        Flowd["B_Ind_temp"]=[]
    Flowd["B_Ind_temp"].append(1)
    if Init==True:
        Vars.append("B_IndP_temp")
        Flowd["B_IndP_temp"]=[]
    Flowd["B_IndP_temp"].append(1)
    if Init==True:
        Vars.append("Perc_B")
        Flowd["Perc_B"]=[]
    Flowd["Perc_B"].append(0)
    #First Bulks######################################################
    for m in range(nbulks):
        BC=str(m+1)
        if Init==True:
            Vars.append(BC+"B_Packets")
            Flowd[BC+"B_Packets"]=[]
        Flowd[BC+"B_Packets"].append(0)
        if Init==True:
            Vars.append(BC+"B_Bytes")
            Flowd[BC+"B_Bytes"]=[]
        Flowd[BC+"B_Bytes"].append(0)
        if Init==True:
            Vars.append(BC+"B_Dur")
            Flowd[BC+"B_Dur"]=[]
        Flowd[BC+"B_Dur"].append(0)
        if Init==True:
            Vars.append(BC+"B_Ind")
            Flowd[BC+"B_Ind"]=[]
        Flowd[BC+"B_Ind"].append(1)
    



def writeflow(iii,Flowd,Dict,Vars,Compflows):
    Bulkpktn=3
    if Flowd["B_Packets_temp"][iii]>Bulkpktn:
        # Add transaction mode ###############################################
        # Add bulk mode ###############################################
        Flowd["B_Counter"][iii]+=1
        Flowd["B_Packets"][iii]+=Flowd["B_Packets_temp"][iii]
        Flowd["B_Bytes"][iii]+=Flowd["B_Bytes_temp"][iii]
        Flowd["B_Dur"][iii]+=Flowd["B_Dur_temp"][iii]
        Flowd["B_Packets_max"][iii]=max([Flowd["B_Packets_max"][iii],Flowd["B_Packets_temp"][iii]])
        Flowd["B_Bytes_max"][iii]=max([Flowd["B_Bytes_max"][iii],Flowd["B_Bytes_temp"][iii]])
        Flowd["B_Dur_max"][iii]=max([Flowd["B_Dur_max"][iii],Flowd["B_Dur_temp"][iii]])
        Flowd["B_Ind"][iii]+=Flowd["B_Ind_temp"][iii]
        linestr=(Dict[iii])
        
    if Flowd["T_Ind"][iii]==True or Flowd["NS:Pack"][iii]+Flowd["NDPack"][iii]<4:
        if Flowd["B_Packets_temp"][iii]<=Bulkpktn:
            Flowd["T_Packets_temp"][iii]+=Flowd["B_Packets_temp"][iii]-1
            #Flowd["T_Bytes_temp"][iii]+=Flowd["B_Bytes_temp"][iii]
        Flowd["T_Counter"][iii]+=1
        Flowd["T_Packets_max"][iii]=max([Flowd["T_Packets_max"][iii],Flowd["T_Packets_temp"][iii]])
        Flowd["T_Bytes_max"][iii]=max([Flowd["T_Bytes_max"][iii],Flowd["T_Bytes_temp"][iii]])
        Flowd["T_Dur_max"][iii]=max([Flowd["T_Dur_max"][iii],Flowd["T_Dur_temp"][iii]])
    
    Flowd["SBytes_av"][iii]=Flowd["SBytes"][iii]/Flowd["NSPack"][iii]
    Flowd["SBytes_std"][iii]=Flowd["SBytes_std"][iii]/Flowd["NSPack"][iii]-Flowd["SBytes_av"][iii]**2
    if Flowd["NDPack"][iii]>0:
        Flowd["DBytes_av"][iii]=Flowd["DBytes"][iii]/Flowd["NDPack"][iii]
        Flowd["DBytes_std"][iii]=Flowd["DBytes_std"][iii]/Flowd["NDPack"][iii]-Flowd["DBytes_av"][iii]**2
    
    Flowd["Curr"][iii]=Flowd["Curr"][iii]-Flowd["Start"][iii]
    Flowd["Inter_av"][iii]=Flowd["Curr"][iii]/(Flowd["NDPack"][iii]+Flowd["NSPack"][iii])
    Flowd["Inter_std"][iii]=(Flowd["Inter_std"][iii]/(Flowd["NSPack"][iii]+Flowd["NDPack"][iii])-
         Flowd["Inter_av"][iii]**2)
    
    if Flowd["NIdle"][iii]>0:
        Flowd["tIdle_av"][iii]=Flowd["tIdle"][iii]/(Flowd["NIdle"][iii])
    
    if Flowd["B_Packets"][iii]>0:
        Flowd["B_Ind"][iii]=Flowd["B_Ind"][iii]/Flowd["B_Counter"][iii]
        Flowd["B_IndP"][iii]=Flowd["B_IndP"][iii]/Flowd["B_Packets"][iii]
        Flowd["Perc_B"][iii]=Flowd["B_Packets"][iii]/(Flowd["NSPack"][iii]+Flowd["NDPack"][iii])
    #del Flowd["B_Dur_temp"][iii], Flowd["B_Bytes_temp"][iii], Flowd["B_Packets_temp"][iii], Flowd["T_Packets_temp"][iii]
    # Write
    linestr=Dict[iii].replace('>',',')
    if (Flowd["B_Ind"][iii]>2):
        print(Flowd["B_Ind"][iii])
    for aa in Vars:
        if not ("temp" in aa):
            linestr+=(","+str(Flowd[aa][iii]))
        del Flowd[aa][iii]
    linestr+="\n"
    Compflows.write(linestr)
    del Dict[iii]



