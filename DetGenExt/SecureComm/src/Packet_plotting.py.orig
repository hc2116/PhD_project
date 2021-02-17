# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 16:57:33 2020

@author: henry
"""

import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 20)
FlowsF=pd.read_csv("Desktop/PhD_project/Data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

FlowsF=pd.read_csv("Desktop/PhD_project/Data/CIC/Friday-WorkingHours.flow")
#FlowsF.head()

FlowsF.columns=[x.strip() for x in FlowsF.columns]
FlowsF.columns=['StartTime', 'protocol', 'SrcAddr', 'src_port', 'DstAddr', 'dst_port',
       'size', 'length', 'npackets']
FlowsF.loc[FlowsF["dst_port"]==20,:].shape

FlowsF['StartTime'] = pd.to_datetime(FlowsF['StartTime'],unit='s') 
FlowsF=FlowsF.sort_values(by="StartTime")


Port=21
SSHComps=FlowsF.loc[FlowsF["dst_port"]==Port,"SrcAddr"].unique()

counter_total=0
counter_add=0
counter_add2=0
for Comps in SSHComps:    
#    Comps=SSHComps[0]
    SFlows=FlowsF.loc[FlowsF["SrcAddr"].isin([Comps])|FlowsF["DstAddr"].isin([Comps]),:]
    ccounter=0
    SFlows = SFlows.assign(time_diff = SFlows['StartTime'].diff())
    SFlows['time_diff_seconds'] = SFlows.time_diff.astype('timedelta64[s]')
    threshold=5
    def create_start_session(x):
        global ccounter
        if np.isnan(x) or x>threshold or x<0 or ccounter>=10:
            ccounter=0
            return(1)
        else:
            ccounter+=1
            return(0)
    SFlows['session_start'] = SFlows.time_diff_seconds.apply(create_start_session)
    SFlows = SFlows.assign(session_id = SFlows['session_start'].cumsum())
    SSH_sessionids=SFlows.loc[SFlows["dst_port"]==Port,"session_id"].unique()
    for ID in SSH_sessionids:
        counter_total+=1
        if len(SFlows.loc[SFlows.session_id==ID,"dst_port"].unique())>1:
            counter_add+=1
        if len(SFlows.loc[SFlows.session_id==ID,"dst_port"].unique())>2:
            counter_add2+=1

print(counter_total)
print(counter_add)
print(counter_add2)
print(counter_add/counter_total)
print(counter_add2/counter_total)


#SFlows["session_id"].value_counts()[SSH_sessionids]

i=0
ID=SSH_sessionids[i]
print(SFlows.loc[SFlows.session_id==ID,['StartTime', 'SrcAddr', 'DstAddr', 'dst_port',]])
i+=1


def set_sessions(df, threshold = 8):
    df2 = df.sort_values(['SrcAddr', 'StartTime'], ascending=[1,1])
    df2 = df2.assign(time_diff = df2['StartTime'].diff())
    df2 = df2.assign(rn = df2.groupby('SrcAddr')['StartTime'].rank(method='first'))
    df2['time_diff_seconds'] = df2.time_diff.astype('timedelta64[s]')
    ccounter=0
    def create_start_session(x):
        global ccounter
        if np.isnan(x) or x>threshold or x<0 or ccounter>=10:
            ccounter=0
            return(1)
        else:
            ccounter+=1
            return(0)
    df2['session_start'] = df2.time_diff_seconds.apply(create_start_session)
    df2 = df2.assign(session_id = df2['session_start'].cumsum())
    
    #df2 = df2.assign(session_id = df2.groupby('SrcAddr')['session_start'].cumsum())
    df3=df2[df2['session_start']==1][['StartTime','SrcAddr','session_id']]
    return(df2,df3)

FlowsF['StartTime'] = pd.to_datetime(FlowsF['StartTime'],unit='s') 
FlowsF,FlowsF_sess_time = set_sessions(FlowsF, threshold = 10)


FlowsF.iloc[0:7,:]
FlowsF["session_id"].value_counts()

SSH_sessionids=FlowsF.loc[FlowsF["dst_port"]==20,"session_id"].unique()


