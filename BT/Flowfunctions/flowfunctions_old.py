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

def Flowcomp(filename,outputfilename,pcap=True, sampling=False):
    if pcap==True:
        Compflowspcap(filename,outputfilename, sampling=sampling)
    else:
        #Compflowstxt(filename,outputfilename)
        print("source other file")
        
        
def Compflowspcap(filename,outputfilename,sampling=False):
    #pingpackets = rdpcap(filename)
    Bulkpktn=3
    MTU=1514
    pingpackets = PcapReader(filename)
    Compflows=open(outputfilename,"w")
    iiiiii=0

    limiter=0
    limiter2=0
    timeout=500
    nbulks=12
    idletime=4    
    Pktnumber=0
    sample_rate=1000
    for line in pingpackets:
        if sampling==True:
            flip = random.randint(1, sample_rate)
            if flip!=1:
                continue
        
        if line.name=="Ethernet":
            line=line.payload
            
        packettime=line.time
        Pktnumber+=1
        #print(" ")
        #print("Pktnumber:"+str(Pktnumber))
        if iiiiii==0:
            if (((line.name in ['IPv6','IP'])|(line.payload.name in ['IPv6','IP']))&(not(
                    ('ICMPv6 Neighbor' in line.payload.name)|
                    ('ICMPv6 Neighbor' in line.payload.payload.name)))):
                iiiiii=1
                if line.payload.name in ['IPv6','IP']:
                    line=line.payload
                if line.payload.name in ['TCP','UDP']:
                    sport=str(line.payload.sport)
                    dport=str(line.payload.dport)
                else:
                    sport='-'
                    dport='-'

                Dict=[str(line.src)+','+str(line.dst)+','+line.payload.name+','+sport+'>'+dport]
                Flowd={}
                Vars=[]

                Vardeclpcap(line,Dict,Flowd,Vars,Init=True,nbulks=nbulks,SDBytes=int(line.len),MTU=MTU,packettime=packettime)
                
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
                Flowd["SBytes_std_broken"][index]+=MTU**2*mt.floor(SByte/MTU)+(SByte-mt.floor(SByte/MTU)*MTU)**2
                Flowd["SBytes_max"][index]=max([Flowd["SBytes_max"][index],SByte])
                Flowd["NSPack"][index]+=1
                Flowd["NSPack_broken"][index]+=mt.ceil(SByte/MTU)
                # Time ###############################################
                Interarr=packettime-Flowd["Curr"][index]
                Flowd["Curr"][index]=packettime
                Flowd["Inter_std"][index]+=Interarr**2
                Flowd["Inter_max"][index]=max([Flowd["Inter_max"][index],Interarr])
                if Interarr>idletime:
                    Flowd["NIdle"][index]+=1
                    Flowd["tIdle"][index]+=Interarr
                    Flowd["tIdle_std"][index]+=Interarr**2
                
                # Test for Bulk mode ###############################################
                # Test if in bulk currently ###############################################
                Bulkchecker(Flowd, index,"S",SByte,Bulkpktn,nbulks,Interarr,MTU)
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    if  (Flowd["FIN1"][index]==False or Flowd["FIN_init"][index]==1) and "F" in str(line.payload.flags):
                        Flowd["FIN1"][index]=True
                        Flowd["FIN_init"][index]=1
                        Flowd["FIN1_SEQN"][index]=line.seq+len(line[TCP].payload)
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and Flowd["FIN_init"][index]==2 and "F" in str(line.payload.flags):
                        Flowd["FIN2"][index]=True
                        Flowd["FIN2_SEQN"][index]=line.seq+len(line[TCP].payload)
                        if Flowd["FIN1_SEQN"][index]+1==line.ack:
                            Flowd["FIN1_ACK"][index]=True
                    elif Flowd["FIN1"][index]==True and "A" in str(line.payload.flags):
                        if Flowd["FIN_init"][index]==1 and Flowd["FIN2_SEQN"][index]+1==line.ack:
                            Flowd["FIN2_ACK"][index]=True
                        if Flowd["FIN_init"][index]==2 and Flowd["FIN1_SEQN"][index]+1==line.ack:
                            Flowd["FIN1_ACK"][index]=True
                        if Flowd["FIN1_ACK"][index]==True and Flowd["FIN2_ACK"][index]==True:
                            writeflow(index,Flowd,Dict,Vars,Compflows,nbulks,Bulkpktn)
            
            # Test if reverse connection is in Dict ###############################################
            elif str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport in Dict:            
                index=Dict.index(str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport)

                # Test for SYN flag ###############################################
                if Flowd["NSPack"][index]==1&(Flowd["NDPack"][index]==0)&Flowd["SYN1"][index]==True:                        
                    Flowd["SYN2"][index]="S" in str(line.payload.flags)

                DByte=int(line.len)
                Flowd["DBytes"][index]+=DByte
                Flowd["DBytes_std"][index]+=DByte**2
                Flowd["DBytes_std_broken"][index]+=MTU**2*mt.floor(DByte/MTU)+(DByte-mt.floor(DByte/MTU)*MTU)**2
                Flowd["DBytes_max"][index]=max([Flowd["DBytes_max"][index],DByte])
                Flowd["NDPack"][index]+=1
                Flowd["NDPack_broken"][index]+=mt.ceil(DByte/MTU)
                # Time #############################################################
                Interarr=packettime-Flowd["Curr"][index]#float(line.time)-Flowd["Curr"][index]
                Flowd["Curr"][index]=packettime#float(line.time)
                Flowd["Inter_std"][index]+=Interarr**2
                Flowd["Inter_max"][index]=max([Flowd["Inter_max"][index],Interarr])
                if Interarr>idletime:
                    Flowd["NIdle"][index]+=1
                    Flowd["tIdle"][index]+=Interarr
                    Flowd["tIdle_std"][index]+=Interarr**2
                       
                # Test for Bulk mode ###############################################
                # Test if in bulk currently ###############################################
                Bulkchecker(Flowd, index,"D",DByte,Bulkpktn,nbulks,Interarr,MTU)
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    if  (Flowd["FIN1"][index]==False or Flowd["FIN_init"][index]==2) and "F" in str(line.payload.flags):
                        Flowd["FIN1"][index]=True
                        Flowd["FIN_init"][index]=2
                        Flowd["FIN1_SEQN"][index]=line.seq+len(line[TCP].payload)
                    elif Flowd["FIN1"][index]==True and Flowd["FIN2"][index]==False and Flowd["FIN_init"][index]==1 and "F" in str(line.payload.flags):
                        Flowd["FIN2"][index]=True
                        Flowd["FIN2_SEQN"][index]=line.seq+len(line[TCP].payload)
                        if Flowd["FIN1_SEQN"][index]+1==line.ack:
                            Flowd["FIN1_ACK"][index]=True
                    elif Flowd["FIN1"][index]==True and "A" in str(line.payload.flags):
                        if Flowd["FIN_init"][index]==2 and Flowd["FIN2_SEQN"][index]+1==line.ack:
                            Flowd["FIN2_ACK"][index]=True
                        if Flowd["FIN_init"][index]==1 and Flowd["FIN1_SEQN"][index]+1==line.ack:
                            Flowd["FIN1_ACK"][index]=True
                        if Flowd["FIN1_ACK"][index]==True and Flowd["FIN2_ACK"][index]==True:
                            writeflow(index,Flowd,Dict,Vars,Compflows,nbulks,Bulkpktn)
                    
             #Flowd,lin
            # Write connection to Dict ###############################################    
            else:
                Dict.append(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                Vardeclpcap(line,Dict,Flowd,[],Init=False,nbulks=nbulks,SDBytes=int(line.len),MTU=MTU,packettime=packettime)
    
        limiter+=1
        limiter2+=1
        if limiter==100000:
            print("Iterations:",limiter2)
            print("Dictionary length:",len(Dict))
            limiter=0
            curtime=packettime#float(line.time)
            for ii in reversed(range(len(Dict))):
                if (curtime-Flowd["Curr"][ii])>timeout:
                    writeflow(ii,Flowd,Dict,Vars,Compflows,nbulks,Bulkpktn)        
    for ii in reversed(range(len(Dict))):
        writeflow(ii,Flowd,Dict,Vars,Compflows) 
    #pingpackets.close()
    Compflows.close()

 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:37:52 2018

@author: henry
"""
def Bulkchecker(Flowd,index,SD,SDByte,Bulkpktn,nbulks,Interarr,MTU):
    if SD=="S":
        Ind=1
    elif SD=="D":
        Ind=2
    else:
        print("Get help")
        return -1
    
    if Flowd["B_Ind_temp"][index]==Ind:
        Flowd["B_IndP_temp"][index]+=Ind
        Flowd["B_IndP_temp_broken"][index]+=mt.ceil(SDByte/MTU)*Ind
        Flowd["B_Packets_temp_broken"][index]+=mt.ceil(SDByte/MTU)
        Flowd["B_Packets_temp"][index]+=1
        Flowd["B_Bytes_temp"][index]+=SDByte
        Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
        
        
        Flowd["T_Packets_temp_temp"][index]+=1
        Flowd["T_Packets_temp_temp_broken"][index]+=mt.ceil(SDByte/MTU)
        Flowd["T_Bytes_temp_temp"][index]+=SDByte
        Flowd["T_Dur_temp_temp"][index]+=Interarr

    # Otherwise delete previous params ###############################################
    elif Flowd["B_Packets_temp_broken"][index]>Bulkpktn:
        # Add transaction mode ###############################################
        if Flowd["T_Ind"][index]==True:
            Flowd["T_Counter"][index]+=1
            Flowd["T_Packets"][index]+=Flowd["T_Packets_temp"][index]
            Flowd["T_Packets_broken"][index]+=Flowd["T_Packets_temp_broken"][index]
            Flowd["T_Packets_std"][index]+=Flowd["T_Packets_temp"][index]**2
            Flowd["T_Packets_broken_std"][index]+=Flowd["T_Packets_temp_broken"][index]**2
            Flowd["T_Packets_max"][index]=max([Flowd["T_Packets_max"][index],Flowd["T_Packets_temp"][index]])
            Flowd["T_Packets_max_broken"][index]=max([Flowd["T_Packets_max_broken"][index],Flowd["T_Packets_temp_broken"][index]])
            Flowd["T_Bytes"][index]+=Flowd["T_Bytes_temp"][index]
            Flowd["T_Bytes_std"][index]+=Flowd["T_Bytes_temp"][index]**2
            Flowd["T_Bytes_max"][index]=max([Flowd["T_Bytes_max"][index],Flowd["T_Bytes_temp"][index]])
            Flowd["T_Dur"][index]+=Flowd["T_Dur_temp"][index]
            Flowd["T_Dur_std"][index]+=Flowd["T_Dur_temp"][index]**2
            Flowd["T_Dur_max"][index]=max([Flowd["T_Dur_max"][index],Flowd["T_Dur_temp"][index]])
        # Add bulk mode ###############################################
        Flowd["B_Counter"][index]+=1
        Flowd["B_Packets"][index]+=Flowd["B_Packets_temp"][index]
        Flowd["B_Packets_broken"][index]+=Flowd["B_Packets_temp_broken"][index]
        Flowd["B_Packets_std"][index]+=Flowd["B_Packets_temp"][index]**2
        Flowd["B_Packets_broken_std"][index]+=Flowd["B_Packets_temp_broken"][index]**2
        Flowd["B_Bytes"][index]+=Flowd["B_Bytes_temp"][index]
        Flowd["B_Bytes_std"][index]+=Flowd["B_Bytes_temp"][index]**2
        Flowd["B_Dur"][index]+=Flowd["B_Dur_temp"][index]
        Flowd["B_Dur_std"][index]+=Flowd["B_Dur_temp"][index]**2
        Flowd["B_Packets_max"][index]=max([Flowd["B_Packets_max"][index],Flowd["B_Packets_temp"][index]])
        Flowd["B_Packets_broken_max"][index]=max([Flowd["B_Packets_broken_max"][index],Flowd["B_Packets_temp_broken"][index]])
        Flowd["B_Bytes_max"][index]=max([Flowd["B_Bytes_max"][index],Flowd["B_Bytes_temp"][index]])
        Flowd["B_Dur_max"][index]=max([Flowd["B_Dur_max"][index],Flowd["B_Dur_temp"][index]])
        Flowd["B_Ind"][index]+=Flowd["B_Ind_temp"][index]
        Flowd["B_IndP"][index]+=Flowd["B_IndP_temp"][index]
        Flowd["B_IndP_broken"][index]+=Flowd["B_IndP_temp_broken"][index]
        # Add first bulks ###############################################
        if Flowd["B_Counter"][index]<=nbulks:
            BC=str(Flowd["B_Counter"][index])
            Flowd[BC+"B_Packets"][index]=Flowd["B_Packets_temp"][index]
            Flowd[BC+"B_Packets_broken"][index]=Flowd["B_Packets_temp_broken"][index]
            Flowd[BC+"B_Bytes"][index]=Flowd["B_Bytes_temp"][index]
            Flowd[BC+"B_Dur"][index]=Flowd["B_Dur_temp"][index]
            Flowd[BC+"B_Ind"][index]=Flowd["B_Ind_temp"][index]
            # Reinitialise params
        Flowd["B_Packets_temp"][index]=1
        Flowd["B_Packets_temp_broken"][index]=mt.ceil(SDByte/MTU)
        Flowd["B_Bytes_temp"][index]=SDByte
        Flowd["B_Dur_temp"][index]=0
        Flowd["B_Ind_temp"][index]=Ind
        Flowd["B_IndP_temp"][index]=Ind
        Flowd["B_IndP_temp_broken"][index]=mt.ceil(SDByte/MTU)*Ind
        
        Flowd["T_Ind"][index]=False
        Flowd["T_Packets_temp_temp"][index]=1
        Flowd["T_Packets_temp_temp_broken"][index]=mt.ceil(SDByte/MTU)
        Flowd["T_Bytes_temp_temp"][index]=SDByte
        Flowd["T_Dur_temp_temp"][index]=Interarr
        
        Flowd["T_Ind_temp"][index]=True
        Flowd["T_Packets_temp"][index]=0
        Flowd["T_Packets_temp_broken"][index]=0
        Flowd["T_Bytes_temp"][index]=0
        Flowd["T_Dur_temp"][index]=0
                        
    else:
        if Flowd["T_Ind_temp"][index]==True:
            Flowd["T_Ind"][index]=True
        Flowd["T_Ind_temp"][index]=True    
        Flowd["T_Packets_temp"][index]+=Flowd["T_Packets_temp_temp"][index]
        Flowd["T_Packets_temp_broken"][index]+=Flowd["T_Packets_temp_temp_broken"][index]
        Flowd["T_Bytes_temp"][index]+=Flowd["T_Bytes_temp_temp"][index]
        Flowd["T_Dur_temp"][index]+=Flowd["T_Dur_temp_temp"][index]
        
        Flowd["T_Packets_temp_temp"][index]=1
        Flowd["T_Packets_temp_temp_broken"][index]=mt.ceil(SDByte/MTU)
        Flowd["T_Bytes_temp_temp"][index]=SDByte
        Flowd["T_Dur_temp_temp"][index]=Interarr
        
        Flowd["B_Packets_temp"][index]=1
        Flowd["B_Packets_temp_broken"][index]=mt.ceil(SDByte/MTU)
        Flowd["B_Bytes_temp"][index]=SDByte
        Flowd["B_Dur_temp"][index]=0
        Flowd["B_Ind_temp"][index]=Ind
        Flowd["B_IndP_temp"][index]=Ind
        Flowd["B_IndP_temp_broken"][index]=mt.ceil(SDByte/MTU)*Ind
    
    
def Vardeclpcap(line,Dict,Flowd,Vars,Init,nbulks,SDBytes,MTU,packettime):   
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
        Vars.append("SBytes_av_broken")
        Flowd["SBytes_av_broken"]=[]
    Flowd["SBytes_av_broken"].append(0)
    if Init==True:
        Vars.append("DBytes")
        Flowd["DBytes"]=[]
    Flowd["DBytes"].append(0)
    if Init==True:
        Vars.append("DBytes_av")
        Flowd["DBytes_av"]=[]
    Flowd["DBytes_av"].append(0)
    if Init==True:
        Vars.append("DBytes_av_broken")
        Flowd["DBytes_av_broken"]=[]
    Flowd["DBytes_av_broken"].append(0)
    if Init==True:
        Vars.append("SBytes_std")
        Flowd["SBytes_std"]=[]
    Flowd["SBytes_std"].append((int(line.len))**2)
    if Init==True:
        Vars.append("DBytes_std")
        Flowd["DBytes_std"]=[]
    Flowd["DBytes_std"].append(0)
    if Init==True:
        Vars.append("SBytes_std_broken")
        Flowd["SBytes_std_broken"]=[]
    Flowd["SBytes_std_broken"].append((int(line.len))**2)
    if Init==True:
        Vars.append("DBytes_std_broken")
        Flowd["DBytes_std_broken"]=[]
    Flowd["DBytes_std_broken"].append(0)
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
    Flowd["Start"].append(float(packettime))#line.time))
    if Init==True:
        Vars.append("Curr")
        Flowd["Curr"]=[]
    Flowd["Curr"].append(float(packettime))#line.time))
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
    if Init==True:
        Vars.append("NSPack_broken")
        Flowd["NSPack_broken"]=[]
    Flowd["NSPack_broken"].append(1)
    if Init==True:
        Vars.append("NDPack_broken")
        Flowd["NDPack_broken"]=[]
    Flowd["NDPack_broken"].append(0)
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
    if Init==True:
        Vars.append("FIN1_SEQN")
        Flowd["FIN1_SEQN"]=[]
    Flowd["FIN1_SEQN"].append(-1)
    if Init==True:
        Vars.append("FIN2_SEQN")
        Flowd["FIN2_SEQN"]=[]
    Flowd["FIN2_SEQN"].append(1)
    if Init==True:
        Vars.append("FIN1_ACK")
        Flowd["FIN1_ACK"]=[]
    Flowd["FIN1_ACK"].append(False)
    if Init==True:
        Vars.append("FIN2_ACK")
        Flowd["FIN2_ACK"]=[]
    Flowd["FIN2_ACK"].append(False)
    #Transaction mode ######################################################
    if Init==True:
        Vars.append("T_Ind")
        Flowd["T_Ind"]=[]
    Flowd["T_Ind"].append(False)
    if Init==True:
        Vars.append("T_Ind_temp")
        Flowd["T_Ind_temp"]=[]
    Flowd["T_Ind_temp"].append(False)
    if Init==True:
        Vars.append("T_Counter")
        Flowd["T_Counter"]=[]
    Flowd["T_Counter"].append(0)
    if Init==True:
        Vars.append("T_Packets")
        Flowd["T_Packets"]=[]
    Flowd["T_Packets"].append(0)
    if Init==True:
        Vars.append("T_Packets_broken")
        Flowd["T_Packets_broken"]=[]
    Flowd["T_Packets_broken"].append(0)
    if Init==True:
        Vars.append("T_Packets_std")
        Flowd["T_Packets_std"]=[]
    Flowd["T_Packets_std"].append(0)
    if Init==True:
        Vars.append("T_Packets_broken_std")
        Flowd["T_Packets_broken_std"]=[]
    Flowd["T_Packets_broken_std"].append(1)
    if Init==True:
        Vars.append("T_Packets_max")
        Flowd["T_Packets_max"]=[]
    Flowd["T_Packets_max"].append(0)
    if Init==True:
        Vars.append("T_Packets_max_broken")
        Flowd["T_Packets_max_broken"]=[]
    Flowd["T_Packets_max_broken"].append(0)
    if Init==True:
        Vars.append("T_Packets_temp")
        Flowd["T_Packets_temp"]=[]
    Flowd["T_Packets_temp"].append(1)
    if Init==True:
        Vars.append("T_Packets_temp_temp")
        Flowd["T_Packets_temp_temp"]=[]
    Flowd["T_Packets_temp_temp"].append(0)
    if Init==True:
        Vars.append("T_Packets_temp_broken")
        Flowd["T_Packets_temp_broken"]=[]
    Flowd["T_Packets_temp_broken"].append(mt.ceil(int(line.len)/MTU))
    if Init==True:
        Vars.append("T_Packets_temp_temp_broken")
        Flowd["T_Packets_temp_temp_broken"]=[]
    Flowd["T_Packets_temp_temp_broken"].append(0)
    if Init==True:
        Vars.append("T_Bytes")
        Flowd["T_Bytes"]=[]
    Flowd["T_Bytes"].append(0)
    if Init==True:
        Vars.append("T_Bytes_std")
        Flowd["T_Bytes_std"]=[]
    Flowd["T_Bytes_std"].append(0)
    if Init==True:
        Vars.append("T_Dur")
        Flowd["T_Dur"]=[]
    Flowd["T_Dur"].append(0)
    if Init==True:
        Vars.append("T_Dur_std")
        Flowd["T_Dur_std"]=[]
    Flowd["T_Dur_std"].append(0)
    if Init==True:
        Vars.append("T_Bytes_max")
        Flowd["T_Bytes_max"]=[]
    Flowd["T_Bytes_max"].append(0)
    if Init==True:
        Vars.append("T_Bytes_temp")
        Flowd["T_Bytes_temp"]=[]
    Flowd["T_Bytes_temp"].append(int(line.len))
    if Init==True:
        Vars.append("T_Bytes_temp_temp")
        Flowd["T_Bytes_temp_temp"]=[]
    Flowd["T_Bytes_temp_temp"].append(0)
    if Init==True:
        Vars.append("T_Dur_max")
        Flowd["T_Dur_max"]=[]
    Flowd["T_Dur_max"].append(0)
    if Init==True:
        Vars.append("T_Dur_temp")
        Flowd["T_Dur_temp"]=[]
    Flowd["T_Dur_temp"].append(0)
    if Init==True:
        Vars.append("T_Dur_temp_temp")
        Flowd["T_Dur_temp_temp"]=[]
    Flowd["T_Dur_temp_temp"].append(0)
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
        Vars.append("B_Packets_temp_broken")
        Flowd["B_Packets_temp_broken"]=[]
    Flowd["B_Packets_temp_broken"].append(mt.ceil(int(line.len)/MTU))
    if Init==True:
        Vars.append("B_Packets")
        Flowd["B_Packets"]=[]
    Flowd["B_Packets"].append(0)
    if Init==True:
        Vars.append("B_Packets_broken")
        Flowd["B_Packets_broken"]=[]
    Flowd["B_Packets_broken"].append(0)
    if Init==True:
        Vars.append("B_Packets_std")
        Flowd["B_Packets_std"]=[]
    Flowd["B_Packets_std"].append(0)
    if Init==True:
        Vars.append("B_Packets_broken_std")
        Flowd["B_Packets_broken_std"]=[]
    Flowd["B_Packets_broken_std"].append(0)
    if Init==True:
        Vars.append("B_Packets_max")
        Flowd["B_Packets_max"]=[]
    Flowd["B_Packets_max"].append(0)
    if Init==True:
        Vars.append("B_Packets_broken_max")
        Flowd["B_Packets_broken_max"]=[]
    Flowd["B_Packets_broken_max"].append(0)
    if Init==True:
        Vars.append("B_Bytes_temp")
        Flowd["B_Bytes_temp"]=[]
    Flowd["B_Bytes_temp"].append(int(line.len))
    if Init==True:
        Vars.append("B_Bytes")
        Flowd["B_Bytes"]=[]
    Flowd["B_Bytes"].append(0)
    if Init==True:
        Vars.append("B_Bytes_std")
        Flowd["B_Bytes_std"]=[]
    Flowd["B_Bytes_std"].append(0)
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
        Vars.append("B_Dur_std")
        Flowd["B_Dur_std"]=[]
    Flowd["B_Dur_std"].append(0)
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
        Vars.append("B_IndP_broken")
        Flowd["B_IndP_broken"]=[]
    Flowd["B_IndP_broken"].append(0)
    if Init==True:
        Vars.append("B_Ind_temp")
        Flowd["B_Ind_temp"]=[]
    Flowd["B_Ind_temp"].append(1)
    if Init==True:
        Vars.append("B_IndP_temp")
        Flowd["B_IndP_temp"]=[]
    Flowd["B_IndP_temp"].append(1)
    if Init==True:
        Vars.append("B_IndP_temp_broken")
        Flowd["B_IndP_temp_broken"]=[]
    Flowd["B_IndP_temp_broken"].append(mt.ceil(int(line.len)/MTU))
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
            Vars.append(BC+"B_Packets_broken")
            Flowd[BC+"B_Packets_broken"]=[]
        Flowd[BC+"B_Packets_broken"].append(0)
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
        
    

def writeflow(iii,Flowd,Dict,Vars,Compflows,nbulks=8,Bulkpktn=3):
    Bulkpktn=3
    linestr=(Dict[iii])
    if Flowd["B_Packets_temp_broken"][iii]>Bulkpktn:
        # Add transaction mode ###############################################
        # Add bulk mode ###############################################
        Flowd["B_Counter"][iii]+=1
        Flowd["B_Packets"][iii]+=Flowd["B_Packets_temp"][iii]
        Flowd["B_Packets_broken"][iii]+=Flowd["B_Packets_temp_broken"][iii]
        Flowd["B_Packets_std"][iii]+=Flowd["B_Packets_temp"][iii]**2
        Flowd["B_Packets_broken_std"][iii]+=Flowd["B_Packets_temp_broken"][iii]**2
        Flowd["B_Bytes"][iii]+=Flowd["B_Bytes_temp"][iii]
        Flowd["B_Bytes_std"][iii]+=Flowd["B_Bytes_temp"][iii]**2
        Flowd["B_Dur"][iii]+=Flowd["B_Dur_temp"][iii]
        Flowd["B_Dur_std"][iii]+=Flowd["B_Dur_temp"][iii]**2
        Flowd["B_Packets_max"][iii]=max([Flowd["B_Packets_max"][iii],Flowd["B_Packets_temp"][iii]])
        Flowd["B_Packets_broken_max"][iii]=max([Flowd["B_Packets_broken_max"][iii],Flowd["B_Packets_temp_broken"][iii]])
        Flowd["B_Bytes_max"][iii]=max([Flowd["B_Bytes_max"][iii],Flowd["B_Bytes_temp"][iii]])
        Flowd["B_Dur_max"][iii]=max([Flowd["B_Dur_max"][iii],Flowd["B_Dur_temp"][iii]])
        Flowd["B_Ind"][iii]+=Flowd["B_Ind_temp"][iii]
        Flowd["B_IndP"][iii]+=Flowd["B_IndP_temp"][iii]
        Flowd["B_IndP_broken"][iii]+=Flowd["B_IndP_temp_broken"][iii]
        
        if Flowd["B_Counter"][iii]<=nbulks:
            BC=str(Flowd["B_Counter"][iii])
            Flowd[BC+"B_Packets"][iii]=Flowd["B_Packets_temp"][iii]
            Flowd[BC+"B_Packets_broken"][iii]=Flowd["B_Packets_temp_broken"][iii]
            Flowd[BC+"B_Bytes"][iii]=Flowd["B_Bytes_temp"][iii]
            Flowd[BC+"B_Dur"][iii]=Flowd["B_Dur_temp"][iii]
            Flowd[BC+"B_Ind"][iii]=Flowd["B_Ind_temp"][iii]
        
    if Flowd["T_Ind"][iii]==True or Flowd["NSPack_broken"][iii]+Flowd["NDPack_broken"][iii]<Bulkpktn:
        if Flowd["B_Packets_temp"][iii]<=Bulkpktn:
            Flowd["T_Packets_temp"][iii]+=Flowd["T_Packets_temp_temp"][iii]
            Flowd["T_Packets_temp_broken"][iii]+=Flowd["T_Packets_temp_temp_broken"][iii]
            Flowd["T_Dur_temp"][iii]+=Flowd["T_Dur_temp_temp"][iii]
            Flowd["T_Bytes_temp"][iii]+=Flowd["T_Bytes_temp_temp"][iii]
            #Flowd["T_Bytes_temp"][iii]+=Flowd["B_Bytes_temp"][iii]
        Flowd["T_Counter"][iii]+=1
        Flowd["T_Packets"][iii]+=Flowd["T_Packets_temp"][iii]
        Flowd["T_Packets_broken"][iii]+=Flowd["T_Packets_temp_broken"][iii]
        Flowd["T_Packets_std"][iii]+=Flowd["T_Packets_temp"][iii]**2
        Flowd["T_Packets_broken_std"][iii]+=Flowd["T_Packets_temp_broken"][iii]**2
        Flowd["T_Packets_max"][iii]=max([Flowd["T_Packets_max"][iii],Flowd["T_Packets_temp"][iii]])
        Flowd["T_Packets_max_broken"][iii]=max([Flowd["T_Packets_max_broken"][iii],Flowd["T_Packets_temp_broken"][iii]])
        Flowd["T_Bytes"][iii]+=Flowd["T_Bytes_temp"][iii]
        Flowd["T_Bytes_std"][iii]+=Flowd["T_Bytes_temp"][iii]**2
        Flowd["T_Bytes_max"][iii]=max([Flowd["T_Bytes_max"][iii],Flowd["T_Bytes_temp"][iii]])
        Flowd["T_Dur"][iii]+=Flowd["T_Dur_temp"][iii]
        Flowd["T_Dur_std"][iii]+=Flowd["T_Dur_temp"][iii]**2
        Flowd["T_Dur_max"][iii]=max([Flowd["T_Dur_max"][iii],Flowd["T_Dur_temp"][iii]])
    
    Flowd["SBytes_av"][iii]=Flowd["SBytes"][iii]/Flowd["NSPack"][iii]
    Flowd["SBytes_av_broken"][iii]=Flowd["SBytes"][iii]/Flowd["NSPack_broken"][iii]
    Flowd["SBytes_std"][iii]=Flowd["SBytes_std"][iii]/Flowd["NSPack"][iii]-Flowd["SBytes_av"][iii]**2
    Flowd["SBytes_std_broken"][iii]=Flowd["SBytes_std_broken"][iii]/Flowd["NSPack_broken"][iii]-Flowd["SBytes_av_broken"][iii]**2
    if Flowd["NDPack"][iii]>0:
        Flowd["DBytes_av"][iii]=Flowd["DBytes"][iii]/Flowd["NDPack"][iii]
        Flowd["DBytes_av_broken"][iii]=Flowd["DBytes"][iii]/Flowd["NDPack_broken"][iii]
        Flowd["DBytes_std"][iii]=Flowd["DBytes_std"][iii]/Flowd["NDPack"][iii]-Flowd["DBytes_av_broken"][iii]**2
        Flowd["DBytes_std_broken"][iii]=Flowd["DBytes_std_broken"][iii]/Flowd["NDPack_broken"][iii]-Flowd["DBytes_av_broken"][iii]**2
    
    Flowd["Curr"][iii]=Flowd["Curr"][iii]-Flowd["Start"][iii]
    Flowd["Inter_av"][iii]=Flowd["Curr"][iii]/(Flowd["NDPack"][iii]+Flowd["NSPack"][iii])
    Flowd["Inter_std"][iii]=(Flowd["Inter_std"][iii]/(Flowd["NSPack"][iii]+Flowd["NDPack"][iii])-Flowd["Inter_av"][iii]**2)
    
    if Flowd["NIdle"][iii]>0:
        Flowd["tIdle_av"][iii]=Flowd["tIdle"][iii]/(Flowd["NIdle"][iii])
        Flowd["tIdle_std"][iii]=(Flowd["tIdle_std"][iii]/(Flowd["NIdle"][iii])-Flowd["tIdle_av"][iii]**2)
    
    if Flowd["B_Packets"][iii]>0:
        Flowd["B_Ind"][iii]=Flowd["B_Ind"][iii]/Flowd["B_Counter"][iii]
        Flowd["B_IndP"][iii]=Flowd["B_IndP"][iii]/Flowd["B_Packets"][iii]
        Flowd["B_IndP_broken"][iii]=Flowd["B_IndP_broken"][iii]/Flowd["B_Packets_broken"][iii]
        Flowd["Perc_B"][iii]=Flowd["B_Packets"][iii]/(Flowd["NSPack"][iii]+Flowd["NDPack"][iii])
        Flowd["B_Packets_std"][iii]=(Flowd["B_Packets_std"][iii]/Flowd["B_Counter"][iii]-
             (Flowd["B_Packets"][iii]/Flowd["B_Counter"][iii])**2)
        Flowd["B_Packets_broken_std"][iii]=(Flowd["B_Packets_broken_std"][iii]/Flowd["B_Counter"][iii]-
             (Flowd["B_Packets_broken"][iii]/Flowd["B_Counter"][iii])**2)
        Flowd["B_Bytes_std"][iii]=(Flowd["B_Bytes_std"][iii]/Flowd["B_Counter"][iii]-
             (Flowd["B_Bytes"][iii]/Flowd["B_Counter"][iii])**2)
        Flowd["B_Dur_std"][iii]=(Flowd["B_Dur_std"][iii]/Flowd["B_Counter"][iii]-
             (Flowd["B_Dur"][iii]/Flowd["B_Counter"][iii])**2)
    if Flowd["T_Counter"][iii]>0:
        Flowd["T_Packets_std"][iii]=(Flowd["T_Packets_std"][iii]/Flowd["T_Counter"][iii]-
             (Flowd["T_Packets"][iii]/Flowd["T_Counter"][iii])**2)
        Flowd["T_Packets_broken_std"][iii]=(Flowd["T_Packets_broken_std"][iii]/Flowd["T_Counter"][iii]-
             (Flowd["T_Packets_broken"][iii]/Flowd["T_Counter"][iii])**2)
        Flowd["T_Bytes_std"][iii]=(Flowd["T_Bytes_std"][iii]/Flowd["T_Counter"][iii]-
             (Flowd["T_Bytes"][iii]/Flowd["T_Counter"][iii])**2)
        Flowd["T_Dur_std"][iii]=(Flowd["T_Dur_std"][iii]/Flowd["T_Counter"][iii]-
             (Flowd["T_Dur"][iii]/Flowd["T_Counter"][iii])**2)
    
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



