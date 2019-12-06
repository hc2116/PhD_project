#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 10:44:26 2018

@author: henry
"""

import pandas as pd
import collections
def ints(a, b):
    return list(range(a, b+1))
def flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


Flows=open("Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt")
Flows=pd.read_table("Desktop/Project/Flow_Clustering_2nd_attempt/Flows.txt",sep=',')

Flows

Flows.iloc[0]


clusterparams=[ints(5,12),ints(14,23)]
CLFlows1=Flows.iloc[0:2,flatten(clusterparams)]
Flows.iloc[0:2,flatten(clusterparams)].iloc[1]
#Flows.iloc[0:2,AA]
clusterparamsB=[ints(5,12),ints(14,23),ints(31,41),47]
Flows.iloc[0:2,flatten(clusterparamsB)]
Flows.iloc[0:2,flatten(clusterparamsB)].iloc[1]

CLFlows1.pl

import numpy as np
