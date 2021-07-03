#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:27:14 2018

@author: henry
"""
import numpy as np
import re
import math as mt
from scapy.all import *

def Flowcomp(filename,outputfilename,pcap=True):
    if pcap==True:
        Compflowspcap(filename,outputfilename)
    else:
        #Compflowstxt(filename,outputfilename)
        print("source other file")
        
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

def Valuewriter(Field, value, write="+",initvalue=0, init=False, First=False, index=0,
                postcalc=False,postcalcVar=False,
                postcalctype=0,postcalcVar2=False):
    
    if postcalc==False:
        if First==True:
            Flowd[Field]=[]
            if Field[0]=="S":
                Flowd["D"+Field[1:]]=[]
            if Field[0]=="D":
                Flowd["S"+Field[1:]]=[]
        if init==True:
            Flowd[Field].append(initvalue)
            if Field[0]=="S":
                Flowd["D"+Field[1:]].append(initvalue)
            if Field[0]=="D":
                Flowd["S"+Field[1:]].append(initvalue)
        elif write=="+":
            Flowd[Field][index]+=value
        elif write=="max":
            Flowd[Field][index]=max(Flowd[Field][index],value)
        elif write=="min":
            Flowd[Field][index]=min(Flowd[Field][index],value)
        elif write=="=":
            Flowd[Field][index]=value
    # Postcalculation
    elif postcalctype==1:
        Flowd[Field][index]=Flowd[Field][index]/(Flowd[postcalcVar][index]+0.00000001)
        if Field[0]=="S":
            Flowd["D"+Field[1:]][index]=Flowd["D"+Field[1:]][index]/(Flowd["D"+postcalcVar[1:]][index]+0.00000001)
        if Field[0]=="D":
            Flowd["S"+Field[1:]][index]=Flowd["S"+Field[1:]][index]/(Flowd["S"+postcalcVar[1:]][index]+0.00000001)
    elif postcalctype==2:
        Flowd[Field][index]=np.sqrt(abs(Flowd[Field][index]/(Flowd[postcalcVar][index]+0.00000001)-Flowd[postcalcVar2][index]**2))
        if Field[0]=="S":
            Flowd["D"+Field[1:]][index]=np.sqrt(abs(Flowd["D"+Field[1:]][index]/(Flowd["D"+postcalcVar[1:]][index]+0.00000001)-Flowd["D"+postcalcVar2[1:]][index]**2))
        if Field[0]=="D":
            Flowd["S"+Field[1:]][index]=np.sqrt(abs(Flowd["S"+Field[1:]][index]/(Flowd["S"+postcalcVar[1:]][index]+0.00000001)-Flowd["S"+postcalcVar2[1:]][index]**2))
    elif postcalctype==3:
        temp1=0
        for x in postcalcVar2:
            temp1+=Flowd[postcalcVar+str(x)][index]
        temp=0
        for x in postcalcVar2:
            temp+=Flowd[postcalcVar+str(x)][index]
            if temp>=temp1/2.0:
                Flowd[Field][index]=x     
                break
        if Field[0]=="S":    
            temp1=0
            for x in postcalcVar2:
                temp1+=Flowd["D"+postcalcVar[1:]+str(x)][index]
            temp=0
            for x in postcalcVar2:
                temp+=Flowd["D"+postcalcVar[1:]+str(x)][index]
                if temp>=temp1/2.0:
                    Flowd["D"+Field[1:]][index]=x     
                    break
        if Field[0]=="D":    
            temp1=0
            for x in postcalcVar2:
                temp1+=Flowd["S"+postcalcVar[1:]+str(x)][index]
            temp=0
            for x in postcalcVar2:
                temp+=Flowd["S"+postcalcVar[1:]+str(x)][index]
                if temp>=temp1/2.0:
                    Flowd["S"+Field[1:]][index]=x     
                    break


def Flowstatsupdater(line,index,packettime, Dir,
                     idletime=4, init=False, First=False,
                     postcalc=False):        
    
    #Packet counter
    Valuewriter("NPack",1,"+",initvalue=1,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"NPack",1,"+",initvalue=1,init=init,First=First,index=index,postcalc=postcalc)
    
    # Bytes
    Byte=int(line.len)
    Valuewriter(Dir+"Bytes",Byte,"+",initvalue=Byte,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Bytes_mean",Byte,"+",initvalue=Byte,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar=Dir+"NPack",
                postcalctype=1)
    Valuewriter(Dir+"Bytes_std",Byte,"+",initvalue=Byte**2,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar=Dir+"NPack",
                postcalctype=2,postcalcVar2=Dir+"Bytes_mean")        
    Valuewriter(Dir+"Bytes_max",Byte,"max",initvalue=Byte,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Bytes_min",Byte,"min",initvalue=Byte,init=init,First=First,index=index,postcalc=postcalc)
    #Median
    Minsize=38
    Maxsize=6000
    Bins=20
    Size_intervals=np.exp(np.linspace(np.log(Minsize),np.log(Maxsize),Bins))
    if init==True:
        for x in Size_intervals:
            Valuewriter(Dir+"Size_inter"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Size_inter"+str(max(Size_intervals[Size_intervals<Byte])),
                1,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Size_median",0,"=",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar=Dir+"Size_inter",
                postcalctype=3,postcalcVar2=Size_intervals)

    # Time ###############################################
    if init==True:
        Valuewriter("Curr",packettime,"=",initvalue=packettime,init=init,First=First,index=index,postcalc=postcalc)
    Interarr=abs(packettime-Flowd["Curr"][index])
    Valuewriter("Curr",packettime,"=",initvalue=packettime,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter("Inter",Interarr,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter("Inter_av",Interarr,"+",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar="NPack",
                postcalctype=1)
    Valuewriter("Inter_std",Interarr**2,"+",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar="NPack",
                postcalctype=2,postcalcVar2="Inter_av")
    Valuewriter("Inter_max",Interarr,"max",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Minsize=0.000
    Maxsize=1
    Bins=20
    Inter_intervals=(np.linspace(np.sqrt(Minsize),np.sqrt(Maxsize),Bins))**2
    if init==True:
        for x in Inter_intervals:
            Valuewriter(Dir+"Inter_inter"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Inter_inter"+str(max(Inter_intervals[Inter_intervals<=Interarr])),
                1,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Inter_median",1,"+",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar=Dir+"Inter_inter",
                postcalctype=3,postcalcVar2=Inter_intervals)

    # Idle periods ###################################    
    Valuewriter("NIdle",Interarr>idletime,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter("tIdle",(Interarr>idletime)*Interarr,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter("tIdle_av",(Interarr>idletime)*Interarr,"+",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar="NIdle",
                postcalctype=1)
    Valuewriter("tIdle_std",(Interarr>idletime)*Interarr**2,"+",initvalue=0,init=init,First=First,index=index,
                postcalc=postcalc,postcalcVar="NIdle",
                postcalctype=2,postcalcVar2="tIdle_av")
    Valuewriter("PUSHflag",("P" in str(line.payload.flags)),"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    
    # Flow periods
    Flow_intervals=np.array([0,1,5,10,30,60,120])
    if init==True:
        for x in Flow_intervals:
            Valuewriter("NPack_interval"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
            Valuewriter(Dir+"NPack_interval"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
            Valuewriter("Bytes_interval"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
            Valuewriter(Dir+"Bytes_interval"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
            Valuewriter(Dir+"Window"+str(x),0,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    
    #print(index)
    #print(Flowd["Inter"][index])
    #print(("NPack_interval"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]]))))
    Valuewriter("NPack_interval"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]])),1,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"NPack_interval"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]])),1,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter("Bytes_interval"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]])),Byte,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Bytes_interval"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]])),Byte,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    Valuewriter(Dir+"Window"+str(max(Flow_intervals[Flow_intervals<=Flowd["Inter"][index]])),line.window,"+",initvalue=0,init=init,First=First,index=index,postcalc=postcalc)
    return Byte, Interarr
    
        
def Flagchecker(line,index, init=False, First=False):
    if init==True:
        Valuewriter("SYN1",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("SYN2",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN1",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN_init",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN1_SEQN",0,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN2",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN2_SEQN",0,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN1_ACK",True,"=",initvalue=False,init=init,First=First,index=index)
        Valuewriter("FIN2_ACK",True,"=",initvalue=False,init=init,First=First,index=index)
        
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
            writeflow(line,index,Flowd,Dict,Vars,Compflows,nbulks,Bulkpktn)

def Compflowspcap(filename,outputfilename):
    #pingpackets = rdpcap(filename)
    Bulkpktn=3
    MTU=1514
    pingpackets = PcapReader(filename)
    Compflows=open(outputfilename,"w")
    iiiiii=0

    limiter=0
    limiter2=0
    timeout=60
    nbulks=12
    idletime=4    
    Pktnumber=0
    global Flowd
    Flowd={}
    Vars=[]
    for line in pingpackets:
        if line.name=="Ethernet":
            line=line.payload
            
        packettime=line.time
        Pktnumber+=1
        #p(" ")
        #p("Pktnumber:"+str(Pktnumber))
        if iiiiii==0:
            sport,dport=payloadchecker(line)
            if sport==False:
                continue
            iiiiii=1
                
            Dict=[str(line.src)+','+str(line.dst)+','+line.payload.name+','+sport+'>'+dport]
            index=Dict.index(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
            Byte, Interarr = Flowstatsupdater(line,index,packettime, Dir="S",
                     idletime=4, init=True, First=True)
            Flagchecker(line,index, init=True, First=True)                
            linestrvars="SIP,DIP,Prot,SPort,DPort"
            Vars=list(Flowd.keys())
            for aa in Vars:
                if not ("temp" in aa):
                    linestrvars+=","+aa
            linestrvars+="\n"
            Compflows.write(linestrvars)

        else:
            sport,dport=payloadchecker(line)
            if sport==False:
                continue
                
            if str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport in Dict:
                index=Dict.index(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                # Bytes ###############################################
                Byte,Interarr=Flowstatsupdater(line=line,index=index,
                                                     packettime=packettime,
                                                     Dir="S",idletime=idletime)                
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    Flagchecker(line,index, Flowd)
            
            # Test if reverse connection is in Dict ###############################################
            elif str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport in Dict:            
                index=Dict.index(str(line.dst)+","+str(line.src)+","+line.payload.name+','+dport+'>'+sport)

                # Test for SYN flag ###############################################
                #if Flowd["SNPack"][index]==1&(Flowd["DNPack"][index]==0)&Flowd["SYN1"][index]==True:                        
                #    Flowd["SYN2"][index]="S" in str(line.payload.flags)
                Byte,Interarr=Flowstatsupdater(line=line,index=index,
                                                     packettime=packettime,
                                                     Dir="D",idletime=idletime)   
                # Test for FIN flag ###############################################
                if line.payload.name=='TCP':    
                    Flagchecker(line,index, Flowd)
                    
            # Write connection to Dict ###############################################    
            else:
                Dict.append(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                index=Dict.index(str(line.src)+","+str(line.dst)+","+line.payload.name+','+sport+'>'+dport)
                Byte, Interarr = Flowstatsupdater(line,index,packettime, Dir="S",
                     idletime=4, init=True, First=False)
                Flagchecker(line,index,init=True)
    
        limiter+=1
        limiter2+=1
        if limiter==100000:
            print("Iterations:",limiter2)
            print("Dictionary length:",len(Dict))
            limiter=0
            curtime=packettime#float(line.time)
            for ii in reversed(range(len(Dict))):
                if (curtime-Flowd["Curr"][ii])>timeout:
                    writeflow(line,ii,Flowd,Dict,Vars,Compflows,nbulks,Bulkpktn)        
    for ii in reversed(range(len(Dict))):
        writeflow(line,ii,Flowd,Dict,Vars,Compflows)
    pingpackets.close()
    Compflows.close()

 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 15:37:52 2018

@author: henry
"""

def writeflow(line,index,Flowd,Dict,Vars,Compflows,nbulks=8,Bulkpktn=3):
    #print("Writing")
    linestr=(Dict[index])
    
    Flowstatsupdater(line=line,index=index,packettime=0, Dir="S",
                     idletime=4, init=False, First=False,
                     postcalc=True)

    # Write
    linestr=Dict[index].replace('>',',')
    for aa in Vars:
        if not ("temp" in aa):
            linestr+=(","+str(Flowd[aa][index]))
        del Flowd[aa][index]
    linestr+="\n"
    Compflows.write(linestr)
    del Dict[index]









def Bulkcheckernew(Flowd,index,SD,SDByte,Bulkpktn,nbulks,Interarr,MTU):
    if SD=="S":
        Ind=1
    elif SD=="D":
        Ind=2
    else:
        print("Get help")
        return -1
    
    if Flowd["B_Ind_temp"][index]==Ind:
        Flowd["B_IndP_temp"][index]+=Ind
        Flowd["B_Packets_temp"][index]+=1
        Flowd["B_Bytes_temp"][index]+=SDByte
        Flowd["B_Dur_temp"][index]+=Interarr*(Flowd["B_Packets_temp"][index]>1.1)
        
        
        Flowd["T_Packets_temp_temp"][index]+=1
        Flowd["T_Bytes_temp_temp"][index]+=SDByte
        Flowd["T_Dur_temp_temp"][index]+=Interarr

    # Otherwise delete previous params ###############################################
    elif Flowd["B_Packets_temp"][index]>Bulkpktn:
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
                        
    else:
        
        Flowd["B_Packets_temp"][index]=1
        Flowd["B_Packets_temp_broken"][index]=mt.ceil(SDByte/MTU)
        Flowd["B_Bytes_temp"][index]=SDByte
        Flowd["B_Dur_temp"][index]=0
        Flowd["B_Ind_temp"][index]=Ind
        Flowd["B_IndP_temp"][index]=Ind
        Flowd["B_IndP_temp_broken"][index]=mt.ceil(SDByte/MTU)*Ind    

def writeflow_old(iii,Flowd,Dict,Vars,Compflows,nbulks=8,Bulkpktn=3):
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
        Flowd["B_Bytes_max"][iii]=max([Flowd["B_Bytes_max"][iii],Flowd["B_Bytes_temp"][iii]])
        Flowd["B_Dur_max"][iii]=max([Flowd["B_Dur_max"][iii],Flowd["B_Dur_temp"][iii]])
        Flowd["B_Ind"][iii]+=Flowd["B_Ind_temp"][iii]
        Flowd["B_IndP"][iii]+=Flowd["B_IndP_temp"][iii]
        
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
        
