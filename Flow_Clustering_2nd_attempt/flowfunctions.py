#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:27:14 2018

@author: henry
"""

def Vardecl(line,Dict,Flowd,Vars=[],Init=False):   
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
    Flowd["T_Bytes_temp"].append(0)
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
    #First Bulks######################################################
    if Init==True:
        Vars.append("1B_Packets")
        Flowd["1B_Packets"]=[]
    Flowd["1B_Packets"].append(0)
    if Init==True:
        Vars.append("1B_Bytes")
        Flowd["1B_Bytes"]=[]
    Flowd["1B_Bytes"].append(0)
    if Init==True:
        Vars.append("1B_Dur")
        Flowd["1B_Dur"]=[]
    Flowd["1B_Dur"].append(0)
    if Init==True:
        Vars.append("1B_Ind")
        Flowd["1B_Ind"]=[]
    Flowd["1B_Ind"].append(1)
    if Init==True:
        Vars.append("Perc_B")
        Flowd["Perc_B"]=[]
    Flowd["Perc_B"].append(0)
    



def writeflow(iii,Flowd,Dict,Vars,Compflows):
    
    if Flowd["B_Packets_temp"][iii]>3:
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
        
    if Flowd["T_Ind"][iii]==True:
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