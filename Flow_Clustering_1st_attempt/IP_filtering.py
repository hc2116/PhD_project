#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 15:51:32 2018

@author: henry
"""

import numpy as np


Comps=["Comp364445","Comp000116", "Comp000219", "Comp000244", "Comp000253", "Comp000577", "Comp000595", "Comp000688",
"Comp000944", "Comp001022", "Comp001050", "Comp001101", "Comp001706", "Comp001884", "Comp002286",
"Comp002466", "Comp002475", "Comp002524", "Comp002760", "Comp002779", "Comp002915", "Comp002930",
"Comp003192", "Comp003403", "Comp003448", "Comp003489", "Comp003602", "Comp003688", "Comp003795",
"Comp004276", "Comp004336", "Comp004355", "Comp004479", "Comp004601", "Comp004603", "Comp004821",
"Comp004852", "Comp004860", "Comp004880", "Comp004959", "Comp005115", "Comp005118", "Comp005295",
"Comp005364", "Comp005591", "Comp005666", "Comp005809", "Comp005823", "Comp005825", "Comp005873",
"Comp005926", "Comp005966", "Comp006069", "Comp006160", "Comp006224", "Comp006396", "Comp006410",
"Comp006420", "Comp006560", "Comp006679", "Comp006850", "Comp007371", "Comp007377", "Comp007434",
"Comp007589", "Comp007753", "Comp007792", "Comp008022", "Comp008056", "Comp008061", "Comp008279",
"Comp008372", "Comp008398", "Comp008581", "Comp008608", "Comp008675", "Comp008789", "Comp008817",
"Comp009032", "Comp009136", "Comp009312", "Comp009410", "Comp009583", "Comp009588", "Comp009700",
"Comp009724", "Comp010016", "Comp010183", "Comp010250", "Comp010338", "Comp010413", "Comp010646",
"Comp010804", "Comp010880", "Comp010933", "Comp011101", "Comp011108", "Comp011116", "Comp011251",
"Comp011278", "Comp011341"]


Flows = open("Desktop/Project/Flow_Clustering_1st_attempt/netflow_day-02")

#line=Flows.readline().split(',')
Compflows=open("Desktop/Project/Flow_Clustering_1st_attempt/Compflows.txt","w")

i=1

for linestr in Flows:
    i+=1
    linestr=Flows.readline()
    line=linestr.split(',')
    if len(line)==11:
        if (line[2] in Comps)|(line[3] in Comps):
            Compflows.write(linestr)
    else:
        print("strange")
        print(line)
        print("strange",linestr)
    #if (line[2] in Comps)|(line[3] in Comps):
    #    Compflows.write(linestr)
    #    Compflows=np.vstack((Compflows, line))        
    if i%1000000==0:
        print(i/1000000,"m lines")
        
print(i)
Flows.close()
Compflows.close()


Flows = open("Desktop/Project/Flow_Clustering_1st_attempt/netflow_day-03")

#line=Flows.readline().split(',')
Compflows=open("Desktop/Project/Flow_Clustering_1st_attempt/Compflows2.txt","w")

i=1

for linestr in Flows:
    i+=1
    linestr=Flows.readline()
    line=linestr.split(',')
    if len(line)==11:
        if (line[2] in Comps)|(line[3] in Comps):
            Compflows.write(linestr)
    else:
        print("strange")
        print(line)
        print("strange",linestr)
    #if (line[2] in Comps)|(line[3] in Comps):
    #    Compflows.write(linestr)
    #    Compflows=np.vstack((Compflows, line))        
    if i%1000000==0:
        print(i/1000000,"m lines")
        
print(i)
Flows.close()
Compflows.close()


Flows = open("Desktop/Project/Flow_Clustering_1st_attempt/netflow_day-04")

#line=Flows.readline().split(',')
Compflows=open("Desktop/Project/Flow_Clustering_1st_attempt/Compflows3.txt","w")

i=1

for linestr in Flows:
    i+=1
    linestr=Flows.readline()
    line=linestr.split(',')
    if len(line)==11:
        if (line[2] in Comps)|(line[3] in Comps):
            Compflows.write(linestr)
    else:
        print("strange")
        print(line)
        print("strange",linestr)
    #if (line[2] in Comps)|(line[3] in Comps):
    #    Compflows.write(linestr)
    #    Compflows=np.vstack((Compflows, line))        
    if i%1000000==0:
        print(i/1000000,"m lines")
        
print(i)
Flows.close()
Compflows.close()