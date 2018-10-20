import pandas as pd
import os
from datetime import datetime
import time
import ctu_botnet_actions
#from models.mchain import *

dataset_path = "/lustre/home/dc002/msdc002/shared/CTU/CTU-13-Dataset/"
#dataset_path = "."

# Computes timestamp and time difference from previous message (using startime of flow)
class DeltaTime:
    def __init__(self):
        self.t = 0
        self._curr_session = 1

   # to apply timedifference to dataset
    def to_timestamp(self,str):
        spl = str.split('.')  
        lt = time.strptime(spl[0], "%Y/%m/%d %H:%M:%S")
        ts = time.mktime(lt)
        return ts + float("0." + spl[1])

    def timediff(self,str):
        ct = self.to_timestamp(str)
        diff = ct - self.t
        self.t = ct
        return diff

    ## split into sessions; default 5 (m?)sec
    def session(self,t,k=5):
        # not that delta time may be negative (presume logging not in order)
        # those are considered to be
        if t > k or t < 0:
            self._curr_session = self._curr_session + 1
        return self._curr_session

# Need all the infected IPs from all experiments:

# experiment 50/51 has in addition the following (52/53 has the 2 first)
IP_50 = ['147.32.84.191','147.32.84.192','147.32.84.193','147.32.84.204',
'147.32.84.205','147.32.84.206','147.32.84.207','147.32.84.208','147.32.84.209']
IP_all = ['147.32.84.165']
infected_ips = IP_all + IP_50


def botnet_tofrom(fname):
    df = pd.read_csv(fname,header=(0))
    df2 = df[df['SrcAddr'].isin(infected_ips) | df['DstAddr'].isin(infected_ips)]
    print("  Adding deltatime\n")
    dt = DeltaTime()
    df2["DeltaTime"] = df2["StartTime"].apply(dt.timediff)
    df2["Session"] = df2["DeltaTime"].apply(dt.session)    
    outfile = fname + "_bot_tofrom.cvs"
    df2.to_csv(outfile)
    print ("Written to file: " + outfile)

def action_by_host(fname):
    df = pd.read_csv(fname,header=(0))
    df2 = df[df['SrcAddr'].isin(infected_ips)]
    print("  Adding deltatime\n")
    dt = DeltaTime()
    df2["DeltaTime"] = df2["StartTime"].apply(dt.timediff)
    df2["Session"] = df2["DeltaTime"].apply(dt.session) 
    actionfile = fname + "_actions.txt"
    write_actions(df2,actionfile)
    print ("Actions written to file: " + actionfile)
    outfile = fname + "_bot_only.cvs"
    df2.to_csv(outfile)
    print ("Updated CVS written to file: " + outfile)

def botnet_only(fname):
    df = pd.read_csv(fname,header=(0))
    df2 = df[df['SrcAddr'].isin(infected_ips)]
    print("  Adding deltatime\n")
    dt = DeltaTime()
    df2["DeltaTime"] = df2["StartTime"].apply(dt.timediff)
    df2["Session"] = df2["DeltaTime"].apply(dt.session) 
    actionfile = fname + "_actions.txt"
    write_actions(df2,actionfile)
    print ("Actions written to file: " + actionfile)
    outfile = fname + "_bot_only.cvs"
    df2.to_csv(outfile)
    print ("Updated CVS written to file: " + outfile)

def benign_one(fname,host):
    dname = "benign_" + host + "_"
    df = pd.read_csv(fname,header=(0))
    df2 = df[df['SrcAddr'] == host]  
    print("  Adding deltatime\n")
    dt = DeltaTime()
    df2["DeltaTime"] = df2["StartTime"].apply(dt.timediff)
    df2["Session"] = df2["DeltaTime"].apply(dt.session) 
    actionfile = dname + "_actions.txt"
    write_actions(df2,actionfile)
    print ("Actions written to file: " + actionfile)
    outfile = dname + "_bot_only.cvs"
    df2.to_csv(outfile)
    print ("Updated CVS written to file: " + outfile)