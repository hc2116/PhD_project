#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 10:07:03 2019

@author: henry
"""

from __future__ import print_function, division
from scapy.all import *


pcap_file_name="data/relay_stepstone-2019-09-11_12-50-38-sc1-1.pcap"
filename="stepping_stone_pairs.csv"

def pcap2csv(pcap_file_name, filename, caplength=300,starttime=6.1):
    
    packets = PcapReader(pcap_file_name)
    fid = open(filename, 'a+')

    sizesup1=[]
    sizesup2=[]
    sizesdown1=[]
    sizesdown2=[]
    
    timesup1=[]
    timesup2=[]
    timesdown1=[]
    timesdown2=[]

    i_sizesup1=0
    i_sizesup2=0
    i_sizesdown1=0
    i_sizesdown2=0
    
    t_prev_up1=0
    t_prev_up2=0
    t_prev_down1=0
    t_prev_down2=0
    
    start_ip="172.16.238.7"
    steppst_ip="172.16.238.8"
    end_ip="172.16.238.9"
    name=pcap_file_name.split('/')[1].split('.')[0]

    i_total=0
    open_flows = dict()   
    
    for line in packets:
        
        if not(line.name=='Ethernet'):
            continue
        t = line.time
        line=line[1]
        
        if not(line.name=='IP'): #
            continue
        if line.payload.name=='Raw': 
            continue
        
        length = line.len
        if (line.proto in [6,17])&('22' in [str(line.sport),str(line.dport)]):
            if (str(line.src) in [start_ip, steppst_ip, end_ip])&(str(line.dst) in [start_ip, steppst_ip, end_ip]):
                five_tuple = tuple([line.proto, line.src + ',' + str(line.sport), line.dst + ',' + str(line.dport)])
        else:
            continue
        
        stored_rec2 = 0
        stored_rec = open_flows.get(five_tuple, None)
        if stored_rec is None:
            stored_rec2 = open_flows.get(tuple([five_tuple[0],five_tuple[2],five_tuple[1]]), None) 
        if stored_rec2 is None: # if already exists
            open_flows[five_tuple] = 'test'
        
        if len(open_flows)>2:
            print("too many connections")
            break

        if i_total==0:
            t_start=t
        i_total+=1
        
        if start_ip in [str(line.src)]:
            t_prev_up1=t-t_prev_up1
            if t-t_start>starttime:
                if i_sizesup1<caplength:
                    sizesup1.append(length)
                    timesup1.append(t-t_prev_up1)
                    t_prev_up1=t
                    i_sizesup1+=1
        if start_ip in [str(line.dst)]:
            t_prev_down1=t-t_prev_down1
            if t-t_start>starttime:
                if i_sizesdown1<caplength:
                    sizesdown1.append(length)
                    timesdown1.append(t-t_prev_down1)
                    t_prev_down1=t
                    i_sizesdown1+=1
   
        if end_ip in [str(line.dst)]:
            t_prev_up2=t-t_prev_up2
            if t-t_start>starttime:
                if i_sizesup2<caplength:
                    sizesup2.append(length)
                    timesup2.append(t-t_prev_up1)
                    t_prev_up2=t
                    i_sizesup2+=1
        if end_ip in [str(line.src)]:
            t_prev_down2=t-t_prev_down2
            if t-t_start>starttime:
                if i_sizesdown2<caplength:
                    sizesdown2.append(length)
                    timesdown2.append(t-t_prev_down1)
                    t_prev_down2=t
                    i_sizesdown2+=1     
        
        if [i_sizesup1,i_sizesup2,i_sizesdown1,i_sizesdown2]==[caplength]*4:
            fid.write(name)
            fid.write(','+','.join(str(e) for e in sizesup1))
            fid.write(','+','.join(str(e) for e in sizesup2))
            fid.write(','+','.join(str(e) for e in sizesdown1))
            fid.write(','+','.join(str(e) for e in sizesdown2))
            
            fid.write(','+','.join(str(e) for e in timesup1))
            fid.write(','+','.join(str(e) for e in timesup2))
            fid.write(','+','.join(str(e) for e in timesdown1))
            fid.write(','+','.join(str(e) for e in timesdown2))
            
            fid.write('\n')
            fid.close()            
            return 0

    if i_sizesup1<caplength:
        sizesup1.extend([0]*(caplength-i_sizesup1))
        timesup1.extend([0]*(caplength-i_sizesup1))
    if i_sizesup2<caplength:
        sizesup2.extend([0]*(caplength-i_sizesup1))
        timesup2.extend([0]*(caplength-i_sizesup1))
    if i_sizesdown1<caplength:
        sizesdown1.extend([0]*(caplength-i_sizesdown1))
        timesdown1.extend([0]*(caplength-i_sizesdown1))
    if i_sizesdown2<caplength:
        sizesdown2.extend([0]*(caplength-i_sizesdown2))
        timesdown2.extend([0]*(caplength-i_sizesdown2))
    print(i_total)
    fid.write(name)
    fid.write(','+','.join(str(e) for e in sizesup1))
    fid.write(','+','.join(str(e) for e in sizesup2))
    fid.write(','+','.join(str(e) for e in sizesdown1))
    fid.write(','+','.join(str(e) for e in sizesdown2))
    
    fid.write(','+','.join(str(e) for e in timesup1))
    fid.write(','+','.join(str(e) for e in timesup2))
    fid.write(','+','.join(str(e) for e in timesdown1))
    fid.write(','+','.join(str(e) for e in timesdown2))
    
    fid.write('\n')
    fid.close()            
    return 0
        
pcap2csv(pcap_file_name, filename)

import os
def loop_folder(folder_name, filename, caplength=300, starttime=6.1):
    """is not quite sucessful right now"""
    import glob
    for pcap_file_name in glob.glob( os.path.join(folder_name, '*.pcap') ):
        print("--> start to process pcap_file_nam: [%s]"%(pcap_file_name))
        pcap2flow2(pcap_file_name,filename,caplength,starttime)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='convert txt file to flows')
    parser.add_argument('-p', '--pcap', default=None,
            help='specify the pcap file you want to process')
    parser.add_argument('-f', '--folder', default=None,
            help='specify the folder you want to loop through')

    parser.add_argument('-t', '--time_out', default=10, type=float,
            help='time out time')

    args = parser.parse_args()
    
    if args.pcap:
        pcap2flow2(args.pcap, args.pcap.rsplit('.pcap')[0] + '.flow', args.time_out)
    elif args.folder:
        loop_folder(args.folder, args.time_out)
    else:
        parser.print_help()