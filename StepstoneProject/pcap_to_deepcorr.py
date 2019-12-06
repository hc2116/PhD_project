#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 10:07:03 2019

@author: henry
"""

from __future__ import print_function, division
from scapy.all import PcapReader


#pcap_file_name="data/relay_stepstone-2019-09-11_12-50-38-sc1-1.pcap"
#pcap_file_name="DeepCorr_Data/Testdata/testdata1_relay_stepstone-2019-09-24_15-38-58-sc1-3.pcap"
#pcap_file_name="tunnel2_relay_stepstone-2019-09-16_16-19-44-sc1-3.pcap"
#pcap_file_name="ssh_stepping_stone_scaled/data/tunnel1_relay_stepstone-2019-09-16_16-14-50-sc1-532.pcap"
#filename="stepping_stone_pairs.csv"

def pcap2csv(pcap_file_name, filename, caplength=300,starttime=12, chafflength=600):
    
    packets = PcapReader(pcap_file_name)
    fid = open(filename+"_Conv.txt", 'a+')
    fidChaff = open(filename+"_Chaff.txt", 'a+')

    sizesup1=[]
    sizesup2=[]
    sizesdown1=[]
    sizesdown2=[]
    
    timesup1=[]
    timesup2=[]
    timesdown1=[]
    timesdown2=[]

    i_sizesup1=-1
    i_sizesup2=-1
    i_sizesdown1=-1
    i_sizesdown2=-1
    
    t_prev_up1=0
    t_prev_up2=0
    t_prev_down1=0
    t_prev_down2=0
    
    i_Chaff1=0
    i_Chaff2=0
    Chaffpackets1=[]
    Chaffpackets2=[]
    
    start_ip="238.7"
    steppst_ip="238.8"
    end_ip="238.9"
    name=pcap_file_name.split('/')[-1].split('.')[0]

    i_total=0
    i_written=0
    open_flows = []
    
    for line in packets:
        if not(line.name=='Ethernet'):
            continue
        t = line.time
        line=line[1]
        
        if not(line.name=='IP'): #
            continue
        if not(line.proto in [6]): #
            continue
        if line.payload.name=='Raw': 
            continue
        
        #t = line.time
        length = line.len
        flags=str(line.flags)
        Src=str(line.src)[7:12]
        Dst=str(line.dst)[7:12]
        
        if (line.proto in [6])&('22' in [str(line.sport),str(line.dport)]):
            if (Src in [start_ip, steppst_ip, end_ip])&(Dst in [start_ip, steppst_ip, end_ip]):
                five_tuple = tuple([line.proto, Src + ':' + str(line.sport), Dst + ':' + str(line.dport)])
        else:
#            print("What?!?")
#            print(line.proto)
#            print(line.sport)
#            print(line.dport)
#            print(Src)
#            print(Dst)
            continue
        if not(five_tuple in open_flows) and not(tuple([five_tuple[0],five_tuple[2],five_tuple[1]]) in open_flows):
            open_flows.append(five_tuple)
        
        if len(open_flows)>2:
            print("too many connections")
            fid.close()            
            return 0

        if i_total==0:
            t_start=t
            i_total+=1
            continue
        i_total+=1
        if t-t_start<starttime:
            continue
        i_written+=1
        
        if start_ip in [Src]:
            if i_sizesup1==-1:
                t_prev_up1=t
                i_sizesup1+=1
                continue
            if i_sizesup1<caplength:
                sizesup1.append(length)
                timesup1.append(t-t_prev_up1)                
                i_sizesup1+=1
            if i_Chaff1<chafflength:
                i_Chaff1+=1
                Chaffpackets1.extend(["S",length,min(t-t_prev_up1,t-t_prev_down1),flags])
            t_prev_up1=t
        if start_ip in [Dst]:
            if i_sizesdown1==-1:
                t_prev_down1=t
                i_sizesdown1+=1
                continue
            if i_sizesdown1<caplength:
                sizesdown1.append(length)
                timesdown1.append(t-t_prev_down1)
                i_sizesdown1+=1
            if i_Chaff1<chafflength:
                i_Chaff1+=1
                Chaffpackets1.extend(["D",length,min(t-t_prev_up1,t-t_prev_down1),flags])
            t_prev_down1=t
            
        if end_ip in [Dst]:
            if i_sizesup2==-1:
                t_prev_up2=t
                i_sizesup2+=1
                continue
            if i_sizesup2<caplength:
                sizesup2.append(length)
                timesup2.append(t-t_prev_up2)
                i_sizesup2+=1
            if i_Chaff2<chafflength:
                i_Chaff2+=1
                Chaffpackets2.extend(["S",length,min(t-t_prev_up2,t-t_prev_down2),flags])
            t_prev_up2=t
        if end_ip in [Src]:
            if i_sizesdown2==-1:
                t_prev_down2=t
                i_sizesdown2+=1
                continue
            if i_sizesdown2<caplength:
                sizesdown2.append(length)
                timesdown2.append(t-t_prev_down2)
                i_sizesdown2+=1     
            if i_Chaff2<chafflength:
                i_Chaff2+=1
                Chaffpackets2.extend(["D",length,min(t-t_prev_up2,t-t_prev_down2),flags])
            t_prev_down2=t
        
        if ([i_sizesup1,i_sizesup2,i_sizesdown1,i_sizesdown2]==[caplength]*4) & ([i_Chaff1,i_Chaff2]==[chafflength]*2):
            xxx='::'.join([str(x) for x in open_flows[0]])
            xxy='::'.join([str(x) for x in open_flows[1]])
            fid.write(name+','+xxx+','+xxy)
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
            print("Full ConvPacket capture")

            xxx='::'.join([str(x) for x in open_flows[0]])
            xxy='::'.join([str(x) for x in open_flows[1]])
            fidChaff.write(name+';'+xxx+';'+xxy)
            fidChaff.write(';'+';'.join(str(e) for e in Chaffpackets1))
            fidChaff.write(';'+';'.join(str(e) for e in Chaffpackets2))
            fidChaff.write('\n')
            fidChaff.close()       
#            print(len(Chaffpackets1))
#            print(len(Chaffpackets2))
            print("Full ChaffPacket capture")
            print("Both captures full")
            return 0
        
    if len(open_flows)<2:
            print("incomplete capture")
            print(open_flows)
            fid.close()            
            return 0
        
    if i_sizesup1<caplength:
        sizesup1.extend([30]*(caplength-i_sizesup1))
        timesup1.extend([-0.01]*(caplength-i_sizesup1))
    if i_sizesup2<caplength:
        sizesup2.extend([30]*(caplength-i_sizesup2))
        timesup2.extend([-0.01]*(caplength-i_sizesup2))
    if i_sizesdown1<caplength:
        sizesdown1.extend([30]*(caplength-i_sizesdown1))
        timesdown1.extend([-0.01]*(caplength-i_sizesdown1))
    if i_sizesdown2<caplength:
        sizesdown2.extend([30]*(caplength-i_sizesdown2))
        timesdown2.extend([-0.01]*(caplength-i_sizesdown2))
    if i_Chaff1<chafflength:
        Chaffpackets1.extend([str(-1)]*(chafflength-i_Chaff1))
    if i_Chaff2<chafflength:
        Chaffpackets2.extend([str(-1)]*(chafflength-i_Chaff2))
    if (i_sizesup1<25)|(i_sizesup2<25)|(i_sizesdown1<25)|(i_sizesdown2<25):
        print("Not enough packets for Conv!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        fid.close()            
        fidChaff.close()            
        return 0
    if (i_Chaff1<25)|(i_Chaff2<25):
        print("Not enough packets for Chaff!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        fid.close()            
        fidChaff.close()            
        return 0
    print("Not full")
    print("Total #packets: "+str(i_total))
    print("Written #packets: "+str(i_written))
    xxx='::'.join([str(x) for x in open_flows[0]])
    xxy='::'.join([str(x) for x in open_flows[1]])
    fid.write(name+','+xxx+','+xxy)
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
    fidChaff.write(name+';'+xxx+';'+xxy)
    fidChaff.write(';'+';'.join(str(e) for e in Chaffpackets1))
    fidChaff.write(';'+';'.join(str(e) for e in Chaffpackets2))
    fidChaff.write('\n')
    fidChaff.close()      
    return 0
        
#filename="test"
#pcap_file_name="../ssh_stepping_stone_scaled/data/tunnel3_relay_stepstone-2019-09-17_17-47-51-sc1-120.pcap"
#pcap2csv(pcap_file_name, filename)

import os
def loop_folder(folder_name, filename, caplength=300, starttime=6.1):
    """is not quite sucessful right now"""
    import glob
    fid = open(filename, 'a+')
    fid.write('name,tuple1,tuple2,')
    fid.write(','.join(['sizesup1']*caplength)+',')
    fid.write(','.join(['sizesup2']*caplength)+',')
    fid.write(','.join(['sizesdown1']*caplength)+',')
    fid.write(','.join(['sizesdown2']*caplength)+',')
    fid.write(','.join(['timesup1']*caplength)+',')
    fid.write(','.join(['timesup2']*caplength)+',')
    fid.write(','.join(['timesdown1']*caplength)+',')
    fid.write(','.join(['timesdown2']*caplength)+'\n')
    fid.close()
    for pcap_file_name in glob.glob( os.path.join(folder_name, '*.pcap') ):
        print("--> start to process pcap_file_name: [%s]"%(pcap_file_name))
        pcap2csv(pcap_file_name,filename,caplength,starttime)


if __name__ == "__main__":
    import argparse
    
    #filename="stepping_stone_pairs.csv"
    caplength=300
    starttime=5

    parser = argparse.ArgumentParser(description='convert txt file to flows')
    parser.add_argument('-p', '--pcap', default=None,
            help='specify the pcap file you want to process')
    parser.add_argument('-f', '--folder', default=None,
            help='specify the folder you want to loop through')
    parser.add_argument('-n', '--name', default=None,
            help='specify the output filename')
    args = parser.parse_args()
    
    filename=args.name
    
    if args.pcap:
        pcap2csv(args.pcap, args.pcap.rsplit('.pcap')[0] + '.csv',caplength,starttime)
    elif args.folder:
        loop_folder(args.folder, filename,caplength,starttime)
    else:
        parser.print_help()