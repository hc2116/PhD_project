'''
   Some helper functions for extracting Sherlock features from different sources and working with
   features 
'''

import numpy as np
import pandas as pd
import scipy
from sherlock_session import *


# not really used as similar functionality inside Reading class more suitable with dataframe    
def percentage_within(first,second,start):
    return float(second - start) / (second - first)

# not really used as similar functionality inside Reading class more suitable with dataframe    
def percentage_outside(first,second,start):
    return 1 - percentage_within(first,second,start)

# not really used as similar functionality inside Reading class more suitable with dataframe    
def sum_session_val(start,end,readings):
    '''
        Computes the sum of the readings between start and end (including percentage of
        overlap with readings)

        Args:
            start: start of session (or first action time)
            end: end of session (or last action time) 
            readings: list of time,value pairs
    '''
    pre_idx = 0 # assumes first is the last reading before session
    sum = readings[pre_idx+1][1] * percentage_within(readings[pre_idx][0],readings[pre_idx+1][0],start)
    i = pre_idx + 2
    while i < len(readings) and reading[i][0] < end:
        sum = sum + readings[i][1]
        i = i + 1
    if i < len(readings):
        end_val = readings[i][1] * percentage_outside(readings[i-1][0],readings[i][0],end)
        sum = sum + end_val
    return sum

# not really used as similar functionality inside Reading class more suitable with dataframe    
def avg_session_val(start,end,readings):
    '''
        Computes the average of the readings between start and end. It includies part that is overlap with reading
        which is achieved by reducing its weight accordingly when computing
        
        Args:
            start: start of session (or first action time)
            end: end of session (or last action time) 
            readings: list of time,value pairs
    '''
    pre_idx = 0 # assumes first is the last reading before session
    sum = [readings[pre_idx+1][1],percentage_within(readings[pre_idx][0],readings[pre_idx+1][0],start)]
    i = pre_idx + 2
    while i < len(readings) and reading[i][0] < end:
        sum = sum + [readings[i][1],1]
        i = i + 1
    if i < len(readings):
        end_val = [readings[i][1],percentage_outside(readings[i-1][0],readings[i][0],end)]
        sum = sum + [end_val]
    #compute avg value w.r.t to weight
    ret = 0
    tot = len(sum)
    for v,w in sum:
        ret = ret + ((v*w)/tot)
    return ret        

# FEATURES
#  note: this is really just ideas of features to extract...

def number_of_actions():
    pass

def T4_total_network():
    pass

def T4_cpu_avg():
    pass

def T4_battery():
    pass

def app_num_threads():
    pass

def app_sms():
    pass

def app_total_network_traffic():
    pass

def app_cpu_usage():
    pass

def app_mem_usage():
    pass

def app_batt_level():
    pass

def app_cpu_usage():
    pass

def app_fun_interrupts():
    pass

def app_stime():
    pass

def app_utime():
    pass

def app_num_threads():
    pass

def sherlock_version():
    pass

'''
    Below are some suggested features. There are no heading in T4/app dataframe so need to use
    indices instead. Below I have for each table
       - listed which features (and their index) I think may be useful
       - indicated how to compute them for each session (average of all readings or total)
'''

# Features from Moriarty session
sess_number_of_actions = -1
sess_total_time = -1
sess_actions_per_time = sess_number_of_actions / sess_total_time

# T4/app indices (auxiliary)

userid = 0
uuid = 1

# T4 indices
total_rec_bytes = 7 # tot
total_rec_packets = 8 # tot
total_trans_bytes = 9 # tot
total_trans_packets = 10 # tot
total_cpu_util = 36 # tot
batt_temp = 28 # avg
total_memory_heap = 40 #avg
tot_proc_user = 102 # acg
tot_proc_kernel = 104 # avg
tot_procs = 111 # avg

# App indices
a_bytes_rec = 6 # tot
a_packets_rec = 7 # tot
a_bytes_trans = 8 # tot
a_packets_trans = 9 # tot
a_threads = 25 # avg
a_rss = 33 # avg
a_stime = 38 # total
a_utime = 40 # total


## testing: requires the various reading files to be in test_data directory. Needs to be changes
if __name__ == "__main__":
    df_t4 = pd.read_csv("test_data/t4_data.txt",delimiter="\t") # T4 table
    df_app = pd.read_csv("test_data/Moriarty_only.txt",delimiter="\t") # Application table
    df_mor = pd.read_csv("test_data/Moriarty_2015_Q4",delimiter="\t") # Moriarty probe
    # TODO: how to sort based on index?
    #df_app = df_app.sort_values([1], ascending=True)
    print(df_mor.shape)
    sess = Session()
    df_mor.apply(lambda row: sess.update_session_time(row[0],row[1],row[6],row[7]),axis=1)
    app_reading = Reading(sess)
    df_app.apply(lambda row: app_reading.set_reading_time(row[0],row[1]),axis=1)
    t4_reading = Reading(sess)
    df_t4.apply(lambda row: t4_reading.set_reading_time(row[0],row[1]),axis=1)
    print (t4_reading.reading_time)
    # TODO: to create FSA etc - see sherlock_actions