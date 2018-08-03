#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:21:34 2018

@author: henry
"""

Packets = open("Desktop/Project/Flow_Clustering_2nd_attempt/Packets2")
Compflows=open("Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt","w")


import pandas as pd
import re

line=Packets.readline().split('","')
line=Packets.readline().split('","')
line

while line[4]!="TCP" or ("Packet size limited" in line[6]):
    line=Packets.readline().split('","')
    
a=line[6].split(" ")
Dict=[line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4]]

Flowdata=pd.DataFrame({"SBytes":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes":[0],
                       "SBytes_std":[(int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))**2],
                       "DBytes_std":[0],
                       "SBytes_max":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes_max":[0],
                       "SBytes_min":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes_min":[0],
                       "Start":[float(line[1])],
                       "Curr":[float(line[1])],
                       "Inter":[0],
                       "#Idle":[0],
                       "tIdle":[0],
                       "#SPack":[1],
                       "#DPack":[0],
                       "SYN1":["SYN" in line[6]],
                       "SYN2":[False],
                       "FIN_init":[0],
                       "FIN1":[False],
                       "FIN2":[False],
                       #"B_Indicator":[1],
                       "B_Counter":[1],
                       "1B_Packets":[0],
                       "1B_Bytes":[0],
                       "1B_Dur":[0],
                       "1B_Ind":[1],
                       "2B_Packets":[0],
                       "2B_Bytes":[0],
                       "2B_Dur":[0],
                       "2B_Ind":[0],
                       "3B_Packets":[0],
                       "3B_Bytes":[0],
                       "3B_Dur":[0],
                       "3B_Ind":[1],
                       "4B_Packets":[0],
                       "4B_Bytes":[0],
                       "4B_Dur":[0],
                       "4B_Ind":[0],
                       "5B_Packets":[0],
                       "5B_Bytes":[0],
                       "5B_Dur":[0],
                       "5B_Ind":[1],
                       "6B_Packets":[0],
                       "6B_Bytes":[0],
                       "6B_Dur":[0],
                       "6B_Ind":[0],
                       "7B_Packets":[0],
                       "7B_Bytes":[0],
                       "7B_Dur":[0],
                       "7B_Ind":[1],
                       "8B_Packets":[0],
                       "8B_Bytes":[0],
                       "8B_Dur":[0],
                       "8B_Ind":[0]})

limiter=0
limiter2=0
timeout=500
nbulks=8

l=0
ll=0
lll=1

import time
time1=0
time2=0
time3=0
time4=0
time5=0
time6=0
time7=0
time8=0
time9=0
time10=0
curtime=time.time()

for lin in Packets:
    #print(line)
    #line=Packets.readline().split('","')
    line=lin.split('","')
    
    if line[4]=="TCP" and (not "Packet size limited" in line[6]):
        curtime=time.time()
        if line[6][1]=="]":
            line[6]=re.sub(r'.*?] ', '', line[6],1)
        a=line[6].split(" ")
        # Test if direct connection is in Dict ###############################################
        if line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4] in Dict:
            l+=1 # To be removed
            index=Dict.index(line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4])
            # Bytes ###############################################
            SBytes=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            Flowdata.loc[index,"SBytes"]+=SBytes
            Flowdata.loc[index,"SBytes_std"]+=SBytes**2
            Flowdata.loc[index,"SBytes_min"]=min([Flowdata.loc[index,"SBytes_min"],SBytes])
            Flowdata.loc[index,"SBytes_max"]=max([Flowdata.loc[index,"SBytes_max"],SBytes])
            Flowdata.loc[index,"#SPack"]=+1
            # Time ###############################################
            Interarr=float(line[1])-Flowdata.loc[index,"Curr"]
            Flowdata.loc[index,"Curr"]=float(line[1])
            Flowdata.loc[index,"Inter"]+=Interarr
            if Interarr>2:
                Flowdata.loc[index,"#Idle"]+=1
                Flowdata.loc[index,"tIdle"]+=Interarr
            
            # Test for Bulk mode ###############################################
            # Test if in bulk currently ###############################################
            BC=str(Flowdata.loc[index,"B_Counter"])
            if Flowdata.loc[index,"B_Counter"]<=nbulks:
                if Flowdata.loc[index,BC+"B_Ind"]==1:
                    Flowdata.loc[index,BC+"B_Packets"]+=1
                    Flowdata.loc[index,BC+"B_Bytes"]+=SBytes
                    Flowdata.loc[index,BC+"B_Dur"]+=Interarr*(Flowdata.loc[index,BC+"B_Packets"]>1.1)
            # Otherwise delete previous params ###############################################
                if Flowdata.loc[index,BC+"B_Packets"]>3:
                    Flowdata.loc[index,"B_Counter"]+=1
                    if Flowdata.loc[index,"B_Counter"]<=nbulks:
                        BC=str(Flowdata.loc[index,"B_Counter"])
                        Flowdata.loc[index,BC+"B_Packets"]+=1
                        Flowdata.loc[index,BC+"B_Bytes"]+=SBytes
                        Flowdata.loc[index,BC+"B_Dur"]+=Interarr*(Flowdata.loc[index,BC+"B_Packets"]>1.1)
                        Flowdata.loc[index,BC+"B_Ind"]=1
                else:
                    Flowdata.loc[index,BC+"B_Packets"]=1
                    Flowdata.loc[index,BC+"B_Bytes"]+=SBytes
                    Flowdata.loc[index,BC+"B_Dur"]=0
                    Flowdata.loc[index,BC+"B_Ind"]=1
                    
                    
            # Test for FIN flag ###############################################
            if  Flowdata.loc[index,"FIN1"]==False and "FIN" in line[6]:
                Flowdata.loc[index,"FIN1"]=True
                Flowdata.loc[index,"FIN_init"]=1
            elif Flowdata.loc[index,"FIN1"]==True and Flowdata.loc[index,"FIN2"]==False and "FIN" in line[6]:
                Flowdata.loc[index,"FIN2"]=True
            elif Flowdata.loc[index,"FIN1"]==True and Flowdata.loc[index,"FIN2"]==True and "ACK" in line[6]:
                linestr=(line[2]+","+line[3]+","+line[4]+","+a[0]+a[2]+a[4]+","+
                         ",".join(Flowdata.iloc[[index]].
                                  to_string(header=False,index=False,index_names=False).split("  ")))+"\n"
                Compflows.write(linestr)
                lll+=1 # To be removed
                del Dict[index]
                print("Delete")
                Flowdata=Flowdata.drop(Flowdata.index[index])
                Flowdata=Flowdata.reset_index(drop=True)
            time1+=time.time()-curtime
            curtime=time.time()
            
            
        # Test if reverse connection is in Dict ###############################################
        elif line[3]+","+line[2]+","+line[4]+","+a[4]+a[2]+a[0] in Dict:            
            curtime=time.time()            
            l+=1 # To be removed
            index=Dict.index(line[3]+","+line[2]+","+line[4]+","+a[4]+a[2]+a[0])

            # Test for SYN flag ###############################################
            if Flowdata.loc[index,"#SPack"]==1&Flowdata.loc[index,"#DPack"]==0&Flowdata.loc[index,"SYN1"]==True:
                        Flowdata.loc[index,"SYN1"]="SYN" in line[6]
            

            Flowdata.loc[index,"DBytes"]+=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            DBytes=int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])
            Flowdata.loc[index,"DBytes"]+=DBytes
            Flowdata.loc[index,"DBytes_std"]+=DBytes**2
            Flowdata.loc[index,"DBytes_min"]=min([Flowdata.loc[index,"DBytes_min"],DBytes])
            Flowdata.loc[index,"DBytes_max"]=max([Flowdata.loc[index,"DBytes_max"],DBytes])
            Flowdata.loc[index,"#DPack"]+=1
            Interarr=float(line[1])-Flowdata.loc[index,"Curr"]
            Flowdata.loc[index,"Curr"]=float(line[1])
            Flowdata.loc[index,"Inter"]+=Interarr
            if Interarr>2:
                Flowdata.loc[index,"#Idle"]+=1
                Flowdata.loc[index,"tIdle"]+=Interarr
            time1+=time.time()-curtime
            curtime=time.time()
            # Test for Bulk mode ###############################################
            # Test if in bulk currently ###############################################
            BC=str(Flowdata.loc[index,"B_Counter"])
            if Flowdata.loc[index,"B_Counter"]<=nbulks:
                if Flowdata.loc[index,BC+"B_Ind"]==2:
                    Flowdata.loc[index,BC+"B_Packets"]+=1
                    Flowdata.loc[index,BC+"B_Bytes"]+=DBytes
                    Flowdata.loc[index,BC+"B_Dur"]+=Interarr*(Flowdata.loc[index,BC+"B_Packets"]>1.1)
            # Otherwise delete previous params ###############################################
                if Flowdata.loc[index,BC+"B_Packets"]>3:
                    Flowdata.loc[index,"B_Counter"]+=1
                    if Flowdata.loc[index,"B_Counter"]<=nbulks:
                        BC=str(Flowdata.loc[index,"B_Counter"])
                        Flowdata.loc[index,BC+"B_Packets"]+=1
                        Flowdata.loc[index,BC+"B_Bytes"]+=DBytes
                        Flowdata.loc[index,BC+"B_Dur"]+=Interarr*(Flowdata.loc[index,BC+"B_Packets"]>1.1)
                        Flowdata.loc[index,BC+"B_Ind"]=2
                else:
                    Flowdata.loc[index,BC+"B_Packets"]=1
                    Flowdata.loc[index,BC+"B_Bytes"]+=DBytes
                    Flowdata.loc[index,BC+"B_Dur"]=0
                    Flowdata.loc[index,BC+"B_Ind"]=2
            time2+=time.time()-curtime
            curtime=time.time()
            # Test for FIN flag ###############################################
            if  Flowdata.loc[index,"FIN1"]==False and "FIN" in line[6]:
                Flowdata.loc[index,"FIN1"]=True
                Flowdata.loc[index,"FIN_init"]=2
            elif Flowdata.loc[index,"FIN1"]==True and Flowdata.loc[index,"FIN2"]==False and "FIN" in line[6]:
                Flowdata.loc[index,"FIN2"]=True
            elif Flowdata.loc[index,"FIN1"]==True and Flowdata.loc[index,"FIN2"]==True and "ACK" in line[6]:
                linestr=(line[3]+","+line[2]+","+line[4]+","+a[4]+a[2]+a[0]+","+
                         ",".join(Flowdata.iloc[[index]].
                                  to_string(header=False,index=False,index_names=False).split("  ")))+"\n"
                Compflows.write(linestr)
                lll+=1 # To be removed
                del Dict[index]
                print("Delete")
                Flowdata=Flowdata.drop(Flowdata.index[index])
                Flowdata=Flowdata.reset_index(drop=True)
            time3+=time.time()-curtime
            curtime=time.time()
            
        # Write connection to Dict ###############################################
        else:
            ll+=1 # To be removed
            Dict.append(",".join(line[2:5])+","+a[0]+a[2]+a[4])
            tempdata=pd.DataFrame({"SBytes":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes":[0],
                       "SBytes_std":[(int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0]))**2],
                       "DBytes_std":[0],
                       "SBytes_max":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes_max":[0],
                       "SBytes_min":[int(line[6].split("Len=")[1].replace('"',' ').split(' ')[0])],
                       "DBytes_min":[0],
                       "Start":[float(line[1])],
                       "Curr":[float(line[1])],
                       "Inter":[0],
                       "#Idle":[0],
                       "tIdle":[0],
                       "#SPack":[1],
                       "#DPack":[0],
                       "SYN1":["SYN" in line[6]],
                       "SYN2":[False],
                       "FIN_init":[0],
                       "FIN1":[False],
                       "FIN2":[False],
                       #"B_Indicator":[1],
                       "B_Counter":[1],
                       "1B_Packets":[0],
                       "1B_Bytes":[0],
                       "1B_Dur":[0],
                       "1B_Ind":[1],
                       "2B_Packets":[0],
                       "2B_Bytes":[0],
                       "2B_Dur":[0],
                       "2B_Ind":[0],
                       "3B_Packets":[0],
                       "3B_Bytes":[0],
                       "3B_Dur":[0],
                       "3B_Ind":[1],
                       "4B_Packets":[0],
                       "4B_Bytes":[0],
                       "4B_Dur":[0],
                       "4B_Ind":[0],
                       "5B_Packets":[0],
                       "5B_Bytes":[0],
                       "5B_Dur":[0],
                       "5B_Ind":[1],
                       "6B_Packets":[0],
                       "6B_Bytes":[0],
                       "6B_Dur":[0],
                       "6B_Ind":[0],
                       "7B_Packets":[0],
                       "7B_Bytes":[0],
                       "7B_Dur":[0],
                       "7B_Ind":[1],
                       "8B_Packets":[0],
                       "8B_Bytes":[0],
                       "8B_Dur":[0],
                       "8B_Ind":[0]})
            Flowdata=Flowdata.append(tempdata,ignore_index=True)
    
    limiter+=1
    limiter2+=1
    if limiter==10000:
        print("Iterations:",limiter2)
        print("Dictionary length:",len(Dict))
        limiter=0
        curtime=float(line[1])
        timeoutflows=Flowdata.index[(curtime-Flowdata["Curr"])>timeout].tolist()
        for ii in reversed(timeoutflows):
            linestr=(Dict[ii]+","+",".join(Flowdata.iloc[[ii]].
                                  to_string(header=False,index=False,index_names=False).split("  ")))+"\n"
            Compflows.write(linestr)
            lll+=1 # To be removed
            del Dict[ii]
            print("Delete")
            Flowdata=Flowdata.drop(Flowdata.index[ii])
            Flowdata=Flowdata.reset_index(drop=True)
            
for ii in range(len(Dict)):
    linestr=(Dict[ii]+","+",".join(Flowdata.iloc[[ii]].
                                  to_string(header=False,index=False,index_names=False).split("  ")))+"\n"
    Compflows.write(linestr)


Packets.close()
Compflows.close()



###################################################################################
Packets.close()
Packets = open("Desktop/Project/Flow_Clustering_2nd_attempt/Packets2")
testing=True

while  testing:
    lin=Packets.readline()
    line=lin.split('","')
    if "TSval" in line[6]:
        print(line)
        testing=False
        


'fasdf asdfadf"asdfasdf'.replace('"',' ').split(' ')
stri='[TCP ACKed unseen segment] 524  >  1077 [ACK] Seq=88053022 Ack=13369719 Win=20144 Len=1460"\n'
re.sub(r'.*?] ', '', stri,1)
