'''
   Functionality to extract actions 
'''
import pandas as pd
from models.mchain import *
import models.ndfsa as mfsa
import models.dfsa as mpta
import os
from datetime import datetime
import time

# idea is to have a debug mode where verbose stuff can be printed but not used much
DEBUG = True
def DEBUG(msg):
    if DEBUG:
        print(msg)

# host that are labelled as infected/botnets or normal in the CTU dataset
infected_hosts = ["147.32.84.165", "147.32.84.191", "147.32.84.192", "147.32.84.193",
                    "147.32.84.204", "147.32.84.205", "147.32.84.206", "147.32.84.207", 
                    "147.32.84.208", "147.32.84.209"]
normal_hosts = ["147.32.84.170", "147.32.84.134", "147.32.84.164", "147.32.87.36",
                  "147.32.80.9", "147.32.87.11"]

class DeltaTime:
    '''
       Class used to compute timestamp and time difference from previous message (using startime of flow)
       Can be used to derive sessions
    '''
    def __init__(self):
        self.t = 0
        self._curr_session = 1

    def to_timestamp(self,str):
        '''
            Generates timestamp
        '''
        spl = str.split('.')  
        lt = time.strptime(spl[0], "%Y/%m/%d %H:%M:%S")
        ts = time.mktime(lt)
        return ts + float("0." + spl[1])

    def timediff(self,str):
        '''
            Computes time difference from previous (current) entry and update current
            requires: sorted by time
        '''
        ct = self.to_timestamp(str)
        diff = ct - self.t
        self.t = ct
        return diff

    ## split into sessions; default 9 (m?)sec
    def session(self,t,k=9):
        '''
            splits data in the sessions; default is when 9 seconds delay
            requires: sorted by time 
        '''
        # Delta time may be negative (presume logging not in order)
        # should not happen when ordered by time though
        if t > k or t < 0:
            self._curr_session = self._curr_session + 1
        return self._curr_session

def sort(df):
    '''
        sort by starttime
    '''
    df = df.sort_values('StartTime', ascending=True)
    return df

def compute_session(df):
    '''
      add sessions and deltatime to dataframe
    '''
    dt = DeltaTime()
    df["DeltaTime"] = df["StartTime"].apply(dt.timediff)
    df["Session"] = df["DeltaTime"].apply(dt.session)
    return df 

def action_of_row(row):
    '''
       Extracts action to be used for particular dataflow entry
         this can be experimented with
    '''
    try: #remove hex format
        port = int(row['Dport'],16)
    except (ValueError,TypeError):
        try: # into integer
            port = int(row['Dport'])
        except (ValueError,TypeError):
            port = -1 # dummy value
    if (row['Proto'] == 'udp' or row['Proto'] == 'tcp') and port == 53:
        action = "dns"
    elif row['Proto'] == 'tcp' and port == 80:
        action = "http"
    else:
        action = row['Proto']
    return action

def session_actions(df):
    '''
        Generates list of list of actions for dataframe:
           each inner list represents a session
           ... so the outer list is a list of sessions.
    '''
    sess, res, curr = 1, [], []
    for index, row in df.iterrows():
        # new session
        if(row['Session'] != sess):
            sess = row['Session']
            #handles dummy sessions
            if curr != []:
                res = res + [curr]
                curr = []
        # assumes port in hex number
        # arbitrary generalise high port numbers
        curr = curr + [action_of_row(row)]
    res = res + [curr]
    return res  


def actions(df):
    '''
        actions grouped by session
    '''
    res = []
    for index, row in df.iterrows():
        res = res + [action_of_row(row)]
    return res  

def actions_str(df, prefix = ''):
    '''
        actions as strings (for printing mainly)
    '''
    acts = actions(df)
    res = ""
    for seq in acts:
        res = res + prefix + "("
        for a in seq:
            res = res + a + ","
        res = res[:-1] + ")\n"
    return res           

def actions_csv(df):
    '''
        Actions as strings in comma-separated format
    '''
    acts = actions(df)
    res = ""
    for seq in acts:
        for a in seq:
            res = res + a + ","
        res = res[:-1] + "\n"
    return res       

def write_actions(df,fname):
    '''
        Write comma separated actions to file
    '''
    acts = actions(df)
    f = open(fname, 'w')
    for seq in acts:
        r = "("
        for a in seq:
            r = r + a + ","
        r = r[:-1] + ")\n"
        f.write(r)
    f.close()

## MARKOV CHAINS

def update_markovchain(mchain,df):
    '''
        Updates a partial MC and updates it with new transitions
        Ignores session: it is only important in corner cases as structure is ignored
          (corner cases are first action of new sessions)
    '''
    prev = mchain.start
    for index, row in df.iterrows():
        act = action_of_row(row)
        mchain.add_trans(prev,act)
        prev = act
    mchain.compute_prob()

def learn_markovchain(df):
    '''
      generates and returns MC from given dataframe
    '''
    df = sort(df)
    mc = MarkovChain()
    update_markovchain(mc,df)
    return mc

def learn_markovchain_by_host(df,filter = lambda *ip : True):
    '''
      Generates MC for each host (source IP)
      filter argument is used to filter out which hosts (IP addr)
      it should be generated MC from
    '''
    df = sort(df)
    res = {}
    grdf = df.groupby(['SrcAddr'])
    for n,hdf in grdf:
        if filter(n):
            mc = learn_markovchain(hdf)
            res[n] = mc
    return res

def learn_single_markovchain_by_host(df,filter = lambda *ip : True):
    '''
        Learn single MC from a set of hosts
          First leans MC for each host and then combines them.
          filter is used to filter IPs to use
    '''
    mcs = learn_markovchain_by_host(df,filter)
    res = MarkovChain()
    for ip in mcs:
        res.combine(mcs[ip])
    return res

## Finite State Automata

def generate_fsa(df,filter = lambda *ip : True):
    '''
        Generates a single FSA for all IPs in the filter
         Achieved host-by-host and then session-by-session
    '''
    df = sort(df)
    pta = mpta.PTA("")
    print ("### generating PTA")
    grdf = df.groupby(['SrcAddr'])
    acts = []
    for n,hdf in grdf:
        if filter(n):
            sdf = compute_session(hdf)
            actions = session_actions(sdf)
            for seq in actions:
                pta.add_action_iter(seq)
    print ("### converting PTA to automata ")
    fsa = mfsa.pta_to_bfndfsa(pta)
    return fsa

# TESTING / SPECIALISED STUFF

def infected_mc(fname):
    df = pd.read_csv(fname,header=(0))
    mc = learn_single_markovchain_by_host(df,lambda ip: ip in infected_hosts)    
    return mc

def normal_mc(fname):
    df = pd.read_csv(fname,header=(0))
    mc = learn_single_markovchain_by_host(df,lambda ip: ip in normal_hosts)    
    return mc

def normal_automata(fname):
    df = pd.read_csv(fname,header=(0))
    fsa = generate_fsa(df,lambda ip: ip in normal_hosts)
    print (len(fsa.states))
    fsa.bluefringe(threshold = 0,strictness=0)
    fsa.merge_leafs()
    mfsa.save_fsa('utp1.json',fsa)
    return fsa

## testing
if __name__ == "__main__":
    fname = 'test_data/test.binetflow.labeled'
    # normal_mc(fname):
    normal_automata(fname)
    #x = mfsa.load_fsa('utp1.json')